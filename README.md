# pyang-as-lib
Use [pyang](https://github.com/mbj4668/pyang) as a library for custom parsing of attributes from YANG models.

## Installation

```bash
cd pyang-as-lib
pip install --upgrade --user pipenv
pipenv --three install
```

## Usage

```bash
pipenv shell
python parse_model.py
# Outputs to testout.json
more testout.json
exit
```

## Sample Output
Per XPath, outputs the:
* Module name
* Qualified XPath
* Cisco XPath derivation
* The absolute, module-based (not prefix), typedef'd (or primitive) data type.
* The primitive YANG data type.
* Description
* Children


```json
{
    "Cisco-IOS-XR-ipv4-bgp-oper:bgp/config-instances/config-instance/config-instance-default-vrf/entity-configurations/entity-configuration/af-independent-config/speaker-id-info/inheritance-chain/bgp-config-entid/neighbor-address/ipv4vpna-mcastddress": {
        "module_name": "Cisco-IOS-XR-ipv4-bgp-oper",
        "xpath": "/ipv4-bgp-oper:bgp/ipv4-bgp-oper:config-instances/ipv4-bgp-oper:config-instance/ipv4-bgp-oper:config-instance-default-vrf/ipv4-bgp-oper:entity-configurations/ipv4-bgp-oper:entity-configuration/ipv4-bgp-oper:af-independent-config/ipv4-bgp-oper:speaker-id-info/ipv4-bgp-oper:inheritance-chain/ipv4-bgp-oper:bgp-config-entid/ipv4-bgp-oper:neighbor-address/ipv4-bgp-oper:ipv4vpna-mcastddress",
        "cisco_xpath": "Cisco-IOS-XR-ipv4-bgp-oper:bgp/config-instances/config-instance/config-instance-default-vrf/entity-configurations/entity-configuration/af-independent-config/speaker-id-info/inheritance-chain/bgp-config-entid/neighbor-address/ipv4vpna-mcastddress",
        "type": "ietf-inet-types:ipv4-address",
        "primitive_type": "string",
        "description": "IPv4 VPN Mcast Addr",
        "children": {}
    },
    "Cisco-IOS-XR-ipv4-bgp-oper:bgp/config-instances/config-instance/config-instance-default-vrf/entity-configurations/entity-configuration/af-independent-config/speaker-id-info/inheritance-chain/bgp-config-entid/address-family-identifier": {
        "module_name": "Cisco-IOS-XR-ipv4-bgp-oper",
        "xpath": "/ipv4-bgp-oper:bgp/ipv4-bgp-oper:config-instances/ipv4-bgp-oper:config-instance/ipv4-bgp-oper:config-instance-default-vrf/ipv4-bgp-oper:entity-configurations/ipv4-bgp-oper:entity-configuration/ipv4-bgp-oper:af-independent-config/ipv4-bgp-oper:speaker-id-info/ipv4-bgp-oper:inheritance-chain/ipv4-bgp-oper:bgp-config-entid/ipv4-bgp-oper:address-family-identifier",
        "cisco_xpath": "Cisco-IOS-XR-ipv4-bgp-oper:bgp/config-instances/config-instance/config-instance-default-vrf/entity-configurations/entity-configuration/af-independent-config/speaker-id-info/inheritance-chain/bgp-config-entid/address-family-identifier",
        "type": "uint8",
        "primitive_type": "uint8",
        "description": "Address family identfier",
        "children": {}
    }
}
