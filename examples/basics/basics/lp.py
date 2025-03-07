# %% [markdown]
# (launchplans)=
#
# # Launch Plans
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Launch plans bind a partial or complete list of inputs necessary to launch a workflow, along
# with optional run-time overrides such as notifications, schedules and more.
# Launch plan inputs must only assign inputs already defined in the reference workflow definition.

# %%
import calendar

# %% [markdown]
# ## When To Use Launch Plans
#
# - For multiple schedules of a workflow with zero or more predefined inputs
# - To run a specific workflow but with a different set of notifications
# - To share a workflow with set inputs with another user, allowing the other user to simply kick off an execution
# - To share a workflow with another user, making sure that some inputs can be overridden if needed
# - To share a workflow with another user, ensuring that some inputs are not changed
#
# Launch plans are the only means for invoking workflow executions.
# A 'default' launch plan will be created during the serialization (and registration process),
# which will optionally bind any default workflow inputs and any default runtime options specified in the project
# flytekit config (such as user role, etc).
#
# The following example creates a default launch plan with no inputs during serialization.
# %%
import datetime

from flytekit import LaunchPlan, current_context, task, workflow


@task
def square(val: int) -> int:
    return val * val


@workflow
def my_wf(val: int) -> int:
    result = square(val=val)
    return result


default_lp = LaunchPlan.get_default_launch_plan(current_context(), my_wf)
square_3 = default_lp(val=3)

# %% [markdown]
# The following shows how to specify a user-defined launch plan that defaults the value of 'val' to 4.
# %%
my_lp = LaunchPlan.create("default_4_lp", my_wf, default_inputs={"val": 4})
square_4 = my_lp()
square_5 = my_lp(val=5)

# %% [markdown]
# It is possible to **fix** launch plan inputs, so that they can't be overridden at execution call time.
# %%
my_fixed_lp = LaunchPlan.get_or_create(name="always_2_lp", workflow=my_wf, fixed_inputs={"val": 2})
square_2 = my_fixed_lp()
# error:
# square_1 = my_fixed_lp(val=1)

# %% [markdown]
# ## Putting It All Together
#
# Default and fixed inputs can be used together to simplify individual executions
# and programmatic ones.
# Here is a simple example to greet each day of the upcoming week:
#

# %%
@task
def greet(day_of_week: str, number: int, am: bool) -> str:
    greeting = "Have a great " + day_of_week + " "
    greeting += "morning" if am else "evening"
    return greeting + "!" * number


@workflow
def go_greet(day_of_week: str, number: int, am: bool = False) -> str:
    return greet(day_of_week=day_of_week, number=number, am=am)


morning_greeting = LaunchPlan.create(
    "morning_greeting",
    go_greet,
    fixed_inputs={"am": True},
    default_inputs={"number": 1},
)

# Let's see if we can convincingly pass a Turing test!
today = datetime.datetime.today()
for n in range(7):
    day = today + datetime.timedelta(days=n)
    weekday = calendar.day_name[day.weekday()]
    if day.weekday() < 5:
        print(morning_greeting(day_of_week=weekday))
    else:
        # We're extra enthusiastic on weekends
        print(morning_greeting(number=3, day_of_week=weekday))
