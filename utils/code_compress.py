from llama_cpp import Llama

llm = Llama(
      model_path="./models/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf",
      chat_format="llama-3",
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      verbose=False,
      # seed=1337, # Uncomment to set a specific seed
      n_ctx=4096, # Uncomment to increase the context window
)

print("Generating a chat completion.")
completion = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant programmer that summarizes code, Summarize args and return type as python annotations. Output in JSON.",
        },
        {"role": "user", "content": """import os.path
import re
from collections import defaultdict

from django.core.exceptions import ViewDoesNotExist
from django.core.management.base import BaseCommand
from django.urls import URLPattern, URLResolver

from core.views import FrontendRouteMixin
from core.views.routes_codegen import is_searchable_in_frontend_general_fulltext_search


def extract_views_from_urlpatterns(urlpatterns, base="/"):
    \"\"\"
    Recursively extract a list of urls and their corresponding views from the urlpatterns.
    \"\"\"
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            try:
                if hasattr(pattern.callback, "view_class"):
                    yield base + str(pattern.pattern), pattern.callback.view_class
                else:
                    yield base + str(pattern.pattern), pattern.callback
            except ViewDoesNotExist:
                continue
        elif isinstance(pattern, URLResolver):
            # Recursive call to explore nested URLConfs
            yield from extract_views_from_urlpatterns(pattern.url_patterns, base + str(pattern.pattern))


def i18n_to_url_param(url):
    return url.replace("/en/", "/<str:lang>/")


def snake_to_camel(snake_str):
    \"\"\"Convert snake_case string to camelCase.\"\"\"
    components = snake_str.split("_")
    # Capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    return components[0] + "".join(x.capitalize() or "_" for x in components[1:])


def extract_params_types_and_convert(input_str):
    \"\"\"
    Extract parameters (with and without specified types) from the input string
    and return them along with the converted string.
    \"\"\"
    # This regex is adjusted to optionally match patterns without specifying a parameter type
    pattern = r"<((?:\\w+:)?\\w+)>"

    # Find all matches of the pattern in the input string
    matches = re.findall(pattern, input_str)
    params_types = []

    # Process each match
    for match in matches:
        # Determine if the parameter had a specified type and replace accordingly
        if ":" in match:
            type_name, param_name = match.split(":")
            # Convert each parameter name from snake_case to camelCase
            camel_case_param_name = snake_to_camel(param_name)
            input_str = input_str.replace(f"<{type_name}:{param_name}>", f":{camel_case_param_name}", 1)
            params_types.append({camel_case_param_name: type_name})
        else:
            camel_case_param = snake_to_camel(match)
            input_str = input_str.replace(f"<{match}>", f":{camel_case_param}", 1)
            params_types.append({camel_case_param: "str"})  # Assuming default type as 'string'

    return input_str, params_types


PATH_PARAM_TO_TS_TYPE = {
    "int": "number",
    "str": "string",
    "uuid": "string",
}


class FrontendRoute:
    def __init__(
        self,
        view,
        path: str,
        params: list[dict[str, str]],
        route_group: str,
        search_tags: list[str] | None = None,
        query_params: list[dict[str, str]] | None = None,
    ):
        self.view = view
        self.path = path
        self.params = params
        self.route_group = route_group
        self.search_tags = search_tags
        self.query_params = query_params

    def __str__(self):
        return f"FrontendRoute(path={self.path}, params={self.params}, route_group={self.route_group}, search_tags={self.search_tags}, query_params={self.query_params})"

    ROUTE_NAME_PREFIX_TO_IGNORE = {
        "portal": ["LangPortalIframeCompanyId"],
        "client": ["LangClientCompanyId", "Lang"],
        "auth": ["Lang"],
    }

    @property
    def path_in_camel(self):
        \"\"\"
        Convert a URL pattern to camelCase format string, handling both
        colon notation, angle-bracket type notation for parameters, and hyphens.
        \"\"\"
        # Remove leading and trailing slashes and remove '?' and everything after it
        url = self.path.split("?")[0].strip("/")

        # Split the URL into parts based on slashes
        parts = url.split("/")

        # Initialize an empty list to hold the processed parts
        camel_case_parts = []

        for part in parts:
            # Check if part is a parameter in angle-bracket notation and extract the parameter name
            if "<" in part and ">" in part:
                part = part[part.find(":") + 1 : part.find(">")]
            # Or if part is a parameter in colon notation and remove the colon
            elif part.startswith(":"):
                part = part[1:]

            # Convert part to camelCase, handling hyphens as part separators
            camel_case = "".join(
                x[0].upper() + x[1:] if len(x) > 1 else x.capitalize() or "_"
                for x in part.replace("-", "_").split("_")
            )
            camel_case_parts.append(camel_case)

        # Combine all parts into a single camelCase string
        camel_case_string = "".join(camel_case_parts)

        if self.route_group in self.ROUTE_NAME_PREFIX_TO_IGNORE:
            for prefix in self.ROUTE_NAME_PREFIX_TO_IGNORE[self.route_group]:
                if camel_case_string.startswith(prefix):
                    camel_case_string = camel_case_string[len(prefix) :]
            camel_case_string = camel_case_string or "_"

        # Ensure the first letter is lowercase
        camel_case_string = camel_case_string[0].lower() + camel_case_string[1:]

        if camel_case_string.endswith("Pk") or camel_case_string.endswith("Id"):
            camel_case_string = camel_case_string[:-2] + "Detail"

        if camel_case_string == "_" or camel_case_string == "":
            camel_case_string = "index"

        return camel_case_string


class FrontendRoutes:
    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns
        self.routes_by_group = defaultdict(list)

    def extract(self):
        for path, view in extract_views_from_urlpatterns(self.urlpatterns):
            try:
                if not issubclass(view, FrontendRouteMixin):
                    continue
            except TypeError:
                if not getattr(view, "frontend_route", False):
                    continue

            if view.query_params:
                path += "?" + "&".join(
                    f"{list(param.keys())[0]}=<{list(param.values())[0]}:{list(param.keys())[0]}>"
                    for param in view.query_params
                )

            path, path_params = extract_params_types_and_convert(i18n_to_url_param(path))

            frontend_route = FrontendRoute(
                view, path, path_params, view.route_group, view.search_tags, view.query_params
            )
            self.routes_by_group[frontend_route.route_group].append(frontend_route)


class Codegen:
    base_directory = "react/routes/codegen"

    def __init__(self, routes: FrontendRoutes, base_directory=None):
        if base_directory:
            self.base_directory = base_directory
        self.routes = routes

    def generate(self):
        raise NotImplementedError


class TypescriptRoutesGenerator(Codegen):
    def route_to_ts(self, route):
        \"\"\"for example: companySetActiveAccount: url<{ id: UUIDField }>('/company/set-active-account/:id/'),\"\"\"
        params_str = ", ".join(
            f"{param_name}: {PATH_PARAM_TO_TS_TYPE[param_type]}"
            for param in route.params
            for param_name, param_type in param.items()
        )
        if params_str:
            params_str = f"<{{ {params_str} }}>"

        return f"  {route.path_in_camel}: url{params_str}('{route.path}'),\n"

    def dump_routes_to_typescript(self, group_name: str):
        result = f\"\"\"import {{ url }} from '../utils';\n\nconst {group_name}Routes = {{\n\"\"\"

        for route in self.routes.routes_by_group[group_name]:
            result += self.route_to_ts(route)

        result += f"}}\n\nexport default {group_name}Routes;\n"
        return result

    def generate(self):
        for route_group, routes in self.routes.routes_by_group.items():
            with open(os.path.join(self.base_directory, f"{route_group}Routes.ts"), "w") as f:
                f.write(self.dump_routes_to_typescript(route_group))


class TypescriptNavigationGenerator(Codegen):
    def generate(self):
        with open(os.path.join(self.base_directory, f"appNavigation.ts"), "w") as f:
            f.write(self.dump_navigation_to_typescript("app"))

    def dump_navigation_to_typescript(self, route_group):
        result = f"import {route_group}Routes from './{route_group}Routes';\n\n"
        result += f"export type NavigationItem = {{\n"
        result += f"  title: string;\n"
        result += f"  url: string;\n"
        result += f"  tags: string[];\n"
        result += f"}};\n\n"
        result += f"const {route_group}Navigation: NavigationItem[] = [\n"

        for route in filter(
            lambda x: is_searchable_in_frontend_general_fulltext_search(x.view),
            self.routes.routes_by_group[route_group],
        ):
            result += f"  {{\n"
            result += f"    title: gettext('{route.view.search_title}'),\n"
            result += f"    url: {route.route_group}Routes.{route.path_in_camel}.url,\n"
            result += (
                f\"\"\"    tags: [{', '.join([f'gettext("{tag}")' for tag in (route.view.search_tags or [])])}],\n\"\"\"
            )
            result += f"  }},\n"

        result += f"];\n\n"
        result += f"export default {route_group}Navigation;\n"
        return result


class Command(BaseCommand):
    help = "Lists all URLs and their corresponding view names."

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-directory",
            dest="base_directory",
            default="react/routes/codegen",
            help="Base directory for output files",
        )

    def handle(self, *args, **kwargs):
        base_directory = kwargs["base_directory"]

        from django.urls import get_resolver

        frontend_route_generator = FrontendRoutes(get_resolver().url_patterns)
        frontend_route_generator.extract()

        TypescriptRoutesGenerator(frontend_route_generator, base_directory).generate()
        TypescriptNavigationGenerator(frontend_route_generator, base_directory).generate()
"""},
    ],
    response_format={
        "type": "json_object",
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "function_name": {
                        "type": "string"
                    },
                    "annotation": {
                        "type": "string"
                    },
                    "what_does_it_do": {
                        "type": "string"
                    }
                },
                "required": ["function_name", "annotation", "what_does_it_do"]
            },
        },
    },
    temperature=0.7,
)

print(completion)

