#!/usr/bin/python
import sys
import json

def main():

    # setup module
    from ansible.module_utils.basic import AnsibleModule
    module = AnsibleModule({
        "egg_path": {"required": True, "type": "path"}
    })

    # append provided egg path to system path for execution
    sys.path.append(module.params["egg_path"])

    # import egg
    from insights_core.core import InsightsCore

    # run egg
    the_core = InsightsCore('json')
    insights_core_json = the_core.run_json()

    # return facts
    module.exit_json(insights_facts=insights_core_json)

if __name__ == "__main__":
    main()