"""
A dedicated helper to manage templates and prompt building.
"""

import json
import os.path as osp
from typing import Union


class Prompter(object):
    __slots__ = ("template", "_verbose")

    def __init__(self, template_name: str = "", verbose: bool = False):
        self._verbose = verbose
            
        file_name = osp.join("templates", f"{template_name}.json")
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        with open(file_name) as fp:
            self.template = json.load(fp)
            
        print(
            f"Using prompt template {template_name}: {self.template['description']}"
        )
            

    def generate_prompt(
        self,
        system: str = "",
        instruction: str = "",
        label: Union[None, str] = None,
    ) -> str:
        # returns the full prompt from instruction and optional input
        # if a label (=response, =output) is provided, it's also appended.
        
        if not system:
            system = self.template['default_system_prompt']

        input = self.template["prompt"].format(
            system=system,
            instruction=instruction
        )

        if self._verbose:
            print(inputs)
        
        if label:
            return {
                "input": input,
                "label": label
            }
        else:
            return {
                "input": inputs
            }

    def get_response(self, output: str) -> str:
        return output \
            .split(self.template["response_split"])[1].strip() \
            .split(self.template['prompt_begin'])[0].strip()