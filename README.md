# Dexter Tools

Tools for importing or manipulating [Dexter](https://github.com/AwestruckStudios/Gen6) Pokémon data.

# Setting up Veekun Pokedex
Install Pokedex with Python virtualenv.

```
> cd veekun-pokedex
> virtualenv ./
> bin/python setup.py develop
```

Generate Pokedex SQLite database.

```
> bin/pokedex load
> bin/pokedex reindex
```
For more information see [Getting-Data](https://github.com/veekun/pokedex/wiki/Getting-Data) on Veekun Pokedex Wiki.