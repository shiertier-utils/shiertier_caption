# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Utility functions for the OpenAI API."""

import json
import logging
import re
import ast

from json_repair import repair_json

log = logging.getLogger(__name__)


def try_parse_ast_to_json(function_string: str) -> tuple[str, dict]:
    """
     # 示例函数字符串
    function_string = "tool_call(first_int={'title': 'First Int', 'type': 'integer'}, second_int={'title': 'Second Int', 'type': 'integer'})"
    :return:
    """

    tree = ast.parse(str(function_string).strip())
    ast_info = ""
    json_result = {}
    # 查找函数调用节点并提取信息
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function_name = node.func.id
            args = {kw.arg: kw.value for kw in node.keywords}
            ast_info += f"Function Name: {function_name}\r\n"
            for arg, value in args.items():
                ast_info += f"Argument Name: {arg}\n"
                ast_info += f"Argument Value: {ast.dump(value)}\n"
                json_result[arg] = ast.literal_eval(value)

    return ast_info, json_result


def try_parse_json_object(input: str) -> tuple[str, dict]:
    """JSON cleaning and formatting utilities."""
    # Sometimes, the LLM returns a json string with some extra description, this function will clean it up.

    result = None
    try:
        # Try parse first
        result = json.loads(input)
    except json.JSONDecodeError:
        log.info("Warning: Error decoding faulty json, attempting repair")

    if result:
        return input, result

    _pattern = r"\{(.*)\}"
    _match = re.search(_pattern, input)
    input = "{" + _match.group(1) + "}" if _match else input

    # Clean up json string.
    input = (
        input.replace("{{", "{")
        .replace("}}", "}")
        .replace('"[{', "[{")
        .replace('}]"', "}]")
        .replace("\\", " ")
        .replace("\\n", " ")
        .replace("\n", " ")
        .replace("\r", "")
        .strip()
    )

    # Remove JSON Markdown Frame
    if input.startswith("```json"):
        input = input[len("```json"):]
    if input.startswith("```"):
        input = input[len("```"):]
    if input.endswith("```"):
        input = input[: len(input) - len("```")]
    # 特殊的，中间未知的"```"后仍有内容，直接移除
    if "```" in input:
        input = input[:input.index("```")]

    try:
        result = json.loads(input)
    except json.JSONDecodeError:
        # Fixup potentially malformed json string using json_repair.
        json_info = str(repair_json(json_str=input, return_objects=False))

        # Generate JSON-string output using best-attempt prompting & parsing techniques.
        try:

            if len(json_info) < len(input):
                json_info, result = try_parse_ast_to_json(input)
            else:
                result = json.loads(json_info)

        except json.JSONDecodeError:
            log.exception("error loading json, json=%s", input)
            return json_info, {}
        else:
            if not isinstance(result, dict):
                log.exception("not expected dict type. type=%s:", type(result))
                return json_info, {}
            return json_info, result
    else:
        return input, result

if __name__ == "__main__":
    test = """```json
{
  "regular": "This image depicts an anime-style character with long, flowing pink hair, wearing a detailed outfit with floral elements. The character is surrounded by various objects, including a lantern, flowers, and candles. The background is dark, with a starry sky visible through a window. The character appears to be in a dreamlike or magical setting, with a serene expression on their face. The overall style is highly detailed and colorful, with a focus on fantasy elements.",
  "midjoury": [
    "Anime character, long pink hair, detailed outfit, floral elements, lantern, flowers, candles, dark background, starry sky, window, dreamlike setting, serene expression, highly detailed, colorful, fantasy elements."
  ],
  "structural": [
    {
      "background": "Dark with a starry sky visible through a window"
    },
    {
      "character": "Anime-style with long pink hair and a detailed outfit"
    },
    {
      "objects": "Lantern, flowers, candles"
    },
    {
      "setting": "Dreamlike or magical"
    },
    {
      "expression": "Serene"
    },
    {
      "style": "Highly detailed and colorful"
    },
    {
      "theme": "Fantasy"
    }
  ],
  "middle": {
    "type1": {
      "character": "Anime-style with long pink hair and a detailed outfit"
    },
    "type2": {
      "objects": "Lantern, flowers, candles"
    },
    "type3": {
      "setting": "Dreamlike or magical"
    }
  },
  "creation": [
    "Start with a dark background and add a starry sky visible through a window",
    "Create an anime-style character with long pink hair and a detailed outfit",
    "Add floral elements to the character's outfit",
    "Place the character in a dreamlike or magical setting",
    "Add a lantern, flowers, and candles around the character",
    "Ensure the character has a serene expression",
    "Use highly detailed and colorful art style",
    "Incorporate fantasy elements throughout the image"
  ],
  "deviantart request": "I would like a commission of an anime-style character with long pink hair and a detailed outfit, surrounded by a lantern, flowers, and candles. The background should be dark with a starry sky visible through a window. The character should have a serene expression and be placed in a dreamlike or magical setting. The art style should be highly detailed and colorful, with a focus on fantasy elements."
}
```"""
    print(try_parse_json_object(test))