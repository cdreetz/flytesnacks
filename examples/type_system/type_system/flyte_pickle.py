# %% [markdown]
# (flyte_pickle)=
#
# # Using Flyte Pickle
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Flyte enforces type safety by leveraging type information to be able to compile
# tasks/workflows, which enables all sorts of nice features (like static analysis of tasks/workflows, conditional branching, etc.)
#
# However, we do also want to provide enough flexibility to end-users so that they don't have to put in a lot of up front
# investment figuring out all the types of their data structures before experiencing the value that flyte has to offer.
#
# Flyte supports FlytePickle transformer which will convert any unrecognized type in type hint to
# FlytePickle, and serialize / deserialize the python value to / from a pickle file.
#
# ## Caveats
#
# Pickle can only be used to send objects between the exact same version of Python,
# and we strongly recommend to use python type that flyte support or register a custom transformer
#
# This example shows how users can custom object without register a transformer.
# %%
from flytekit import task, workflow


# %% [markdown]
# `People` is a user defined complex type, which can be used to pass complex data between tasks.
# We will serialize this class to a pickle file and pass it between different tasks.
#
# :::{Note}
# Here we can also {ref}`turn this object to dataclass <dataclass_type>` to have better performance.
# We use simple object here for demo purpose.
# You may have some object that can't turn into a dataclass, e.g. NumPy, Tensor.
# :::
# %%
class People:
    def __init__(self, name):
        self.name = name


# %% [markdown]
# Object can be returned as outputs or accepted as inputs
# %%
@task
def greet(name: str) -> People:
    return People(name)


@workflow
def welcome(name: str) -> People:
    return greet(name=name)


if __name__ == "__main__":
    """
    This workflow can be run locally. During local execution also,
    the custom object (People) will be marshalled to and from python pickle.
    """
    welcome(name="Foo")


from typing import List

# %% [markdown]
# By default, if the list subtype is unrecognized, a single pickle file is generated.
# To also improve serialization and deserialization performance for cases with millions of items or large list items,
# users can specify a batch size, processing each batch as a separate pickle file.
# Example below shows how users can set batch size.
#
# %%
from flytekit.types.pickle.pickle import BatchSize
from typing_extensions import Annotated


@task
def greet_all(names: List[str]) -> Annotated[List[People], BatchSize(2)]:
    return [People(name) for name in names]


@workflow
def welcome_all(names: List[str]) -> Annotated[List[People], BatchSize(2)]:
    return greet_all(names=names)


if __name__ == "__main__":
    """
    In this example, two pickle files will be generated:
    - One containing two People objects
    - One containing one People object
    """
    welcome_all(names=["f", "o", "o"])
