a composable context is a repository with a conventional folder structure, containing mainly gitignored `.cache` for fetched data and knowledge from external sources, and a src scratch pad for quick experimentations, a memory for episodic investigations worth sharing, a knowledge_base with curated content, and src folder with `./src/specification/` for spec driven development of scripts. scripts are managed with classical packages managers uv, npm, ...

A context has tow promotion ladders, one for code from ./cache/src to ./src one the code is proven to have reuse benefit, and one for knowledge from .cache to memory and to knowledge_base, from the knowledge_base it is also possible to curate content that gets exported to external sources closing a loop of knowledge feedback.

A context repo is therefore a colelction of skills, source code and knowledge that are maintained by an owning entity and therefore represent a consolidated quality gate higher than users selecting every single skill and dependency.

A context composition is one context importing another one through a manifest. The composition is independent from the code packages management and flattens the content of all imported context repositories to create a unified navigable surface. That means eve if in a first scenario context-repo-A imported context-repo-B, in another context-repo B could import context-repo-A which would result in the same surface visible to the user's agentic workflow.

