"""Attempt to use pyang like a library.
Mostly extracted from bin/pyang.
Should probably contribute this back. :)
Does not handle deviations or hello.
"""
import pdb
import os
import json
import logging
from pyang import Context, FileRepository
from pyang.yang_parser import YangParser
from pyang import syntax
from pyang import statements
from pyang import error

def get_type(node):
    """Gets the immediate, top-level type of the node.
    """
    type_obj = node.search_one('type')
    type_name = None
    if type_obj is not None:
        type_name = type_obj.arg
    return type_name

def get_primitive_type(node):
    """Recurses through the typedefs and returns
    the most primitive YANG type defined.
    """
    type_obj = node.search_one('type')
    primitive_type = None
    def recurse_typedefs(node):
        typedef = node.arg if node else None
        if hasattr(node, 'i_typedef'):
            typedef_obj = node.i_typedef
            if typedef_obj:
                typedef = get_primitive_type(typedef_obj)
        return typedef
    primitive_type = recurse_typedefs(type_obj)
    return primitive_type

def recurse_children(node, module):
    """Recurses through module levels and extracts
    xpath, type, primitive types, and children.
    """
    if not hasattr(node, 'i_children'):
        return {}
    children = (child for child in node.i_children if child.keyword in statements.data_definition_keywords)
    parsed_children = {}
    for child in children:
        xpath = statements.mk_path_str(child, with_prefixes=False)
        fq_xpath = '%s:%s' % (module.arg, xpath[1:])
        parsed_children[fq_xpath] = {
            'type': get_type(child),
            'primitive_type': get_primitive_type(child),
            'children': recurse_children(child, module)
        }
    return parsed_children

# Let's begin..
base_data_dir = 'testdata/'
model_filenames = ['Cisco-IOS-XR-ipv4-bgp-oper.yang']
# Context has a dependency on Repository
# Repository is abstract, only FileRepository exists
file_repository = FileRepository(path=base_data_dir, use_env=False, no_path_recurse=False)
# Contexts are like the base controller for parsing in pyang
context = Context(repository=file_repository)
parser = YangParser()
# YangParser has a dependency on Context
# Context also has a dependency on YangParser
# Parse all the models in to modules
modules = []
for filename in model_filenames:
    model_file_path = os.path.join(base_data_dir, filename)
    model_data = None
    with open(model_file_path, 'r') as model_fd:
        model_data = model_fd.read()
    # Some model filenames indicate revision, etc.
    filename_attributes = syntax.re_filename.search(filename)
    module = None
    if filename_attributes is None:
        module = context.add_module(filename, model_data)
    else:
        (name, revision, model_format) = filename_attributes.groups()
        module = context.add_module(
            filename, model_data, name, revision, model_format,
            expect_failure_error=False
        )
    modules.append(module)
# Some kind of validation step?
context.validate()
# Validating features?
for module in modules:
    if module.arg in context.features:
        for feature in context.features[module.arg]:
            if feature not in module.i_features:
                raise Exception('FEATURE %s MISSING IN %s' % (feature, module.arg))
# Now check for errors?
# Sort our errors.
def keyfun(e):
    if e[0].ref == model_filenames[0]:
        return 0
    else:
        return 1

context.errors.sort(key=lambda e: (e[0].ref, e[0].line))
if len(model_filenames) > 0:
    # Print errors in filename order.
    # TODO: Pretty sure this doesn't make sense.
    context.errors.sort(key=keyfun)

# Parse out all the module names for error checking.
module_names = []
for module in modules:
    module_names.append(module.arg)
    for included_module in module.search('include'):
        module_names.append(included_module.arg)

# Now actually do error parsing
for (epos, etag, eargs) in context.errors:
    if (context.implicit_errors == False and
        hasattr(epos.top, 'i_modulename') and
        epos.top.arg not in module_names and
        epos.top.i_modulename not in module_names and
        epos.ref not in model_filenames):
        # this module was added implicitly (by import); skip this error
        # the code includes submodules
        continue
    elevel = error.err_level(etag)
    if error.is_warning(elevel):
        kind = "error"
        exit_code = 1
    logging.error('%s: %s: %s', str(epos), kind, etag)

# Now actually do whatever we want.
parsed_modules = [recurse_children(module, module) for module in modules]
if len(parsed_modules) == 1:
    parsed_modules = parsed_modules[0]
with open('testout.json', 'w') as testout_fd:
    json.dump(parsed_modules, testout_fd)
