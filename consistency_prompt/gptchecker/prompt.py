####################################
# Data relationship
####################################

DATA_RELATIONSHIP_SYSTEM = """
# Identity
You are a software engineer that is extremely good at analyzing frontend code, understand its flow control and logic, and construct hierarchical call graphs.
At each turn, you should first provide your step-by-step thinking for solving the task. Your thought process should be enclosed using "<thought>" tag.
"""

DATA_RELATIONSHIP_USER = """
# Task
This is the log after we run the same {traces} multiple times (Or only one time):

{logs}

Based on the logs, identify all traces with data dependency in a hierarchical order.
A data dependency is a situation in which an service refers to the data of a preceding service.

# Guidelines
- You MUST use " > " to separate the parent and dependent traces
- You MUST enclose each parent-dependent service with a "<edge>" tag
- You MUST have as much coverage as possible
- You MUST NOT HAVE repeated dependency in the answer
- An example: <edge>class.method > class.method</edge>
"""

####################################
# Trigger relationship
####################################

TRIGGER_RELATIONSHIP_SYSTEM = """
# Identity
You are a software engineer that is extremely good at analyzing frontend code, understand its flow control and logic, and construct hierarchical call graphs.
At each turn, you should first provide your step-by-step thinking for solving the task. Your thought process should be enclosed using "<thought>" tag.
"""

TRIGGER_RELATIONSHIP_USER = """
# Task
Here is the concatenated code snippet with all API calls we are interested in:

{code}

Based on the code, identify all possible parent-child API call relationships in a hierarchical order.

# Guidelines
- You MUST use " > " to separate the parent and child APIs
- You MUST enclose each parent-child API call with a "<trigger>" tag
- Your solution must have as much coverage as possible
- An example: <trigger>/api/version/service/parent > /api/version/service/child</trigger>
"""

####################################
# Input constraint
####################################

INPUT_CONSTRAINT_SYSTEM = """
# Identity
You are a software engineer that is extremely good at modelling entity relationships in databases.
You are responsible for checking how two different classes are related to each other.
At each turn, you need to do THREE things:
1. You SHOULD first provide your step-by-step thinking for solving the task. Your thought process should be enclosed using "<thought>" tag. 
2. You SHOULD construct as many of the most important first-order logic constraints and output it in general format. Examples:
    - ∀x (isDog(x) → hasFourLegs(x)
    - ∃x (isCat(x) ∧ isBlack(x))
    - ∀x (isPerson(x) → ∃y (isDog(y) ∧ owns(x, y)))
    - ∀x ∀y ((isParent(x, y) ∧ isMale(x)) → isFather(x, y))
    - ∃x (isHuman(x) ∧ loves(x, Mary)),
    - ∀x (isStudent(x) ∧ studiesHard(x) → getsGoodGrades(x))
    - ∀x (isAnimal(x) → (∃y (isFood(y) ∧ eats(x, y))))
)
3. You SHOULD write a function in a block of Python code to solve the task based on the constraints.
"""

INPUT_CONSTRAINT_USER = """
# Task
Here are the definition of two classes [A] and [B]:

Class [A] and its attributes:

{class_definition1}

Class [B] and its attributes:

{class_definition2}

Instances of both classes [A] and [B] can be found in these logs:

{logs}

Based on the logs, infer the possible relationships of attributes in [A] and [B] by referencing these common types of relationships:
1. Foreign key: an attribute in an entity that references the primary key attribute in another entity, both attributes must be the same data type.
2. Primary key: attribute(s) that can uniquely identify entities in an entity set.
3. Matching: an attribute(E.g: Price, ID) in an entity that must have the same value as an attribute in another entity, both attributes must be the same data type. (E.g: Price, ID)

Then, write a function that determines if instances of [A] and [B] are related to each other using their attributes.

# Guidelines
- You MUST treat an object instance as a dict in your function. 
- You MUST use the function signature `def is_related(instance_A: dict, instance_B: dict) -> bool`.
- YOU DONT HAVE TO use all attributes of [A] and [B] in your function for matching. If an attribute is not helpful for matching, you can OMIT it.
- DO NOT output any code that is not related to the function, such as test cases.
"""

INPUT_CONSTRAINT_FEEDBACK = """
Your code failed {fails} test cases. There should be AT LEAST ONE MATCH. Please RELAX THE CONSTRAINTS to match instances from [A] to [B], and try again.

{reasons}
"""

####################################
# Flow constraint
####################################

FLOW_CONSTRAINT_SYSTEM = """
# Identity
You are a software engineer that is extremely good at flow control and logic.
At each turn, you should first provide your step-by-step thinking for solving the task. Your thought process should be enclosed using "<thought>" tag.
After that, you should use write a function in a block of Python code to solve the task.
"""

FLOW_CONSTRAINT_USER = """
# Task
After calling {parent_url}, the client can either call branch [A] or [B]:

[A] {child_url1}, which produces these logs:

{logs1}

[B] {child_url2}, which produces these logs:

{logs2}

Based on the logs produced by branches [A] and [B], 
Identify the most important first-order logic constraints that causes the program to switch from branch [A] to [B] and output it in general format(eg: ∀x (isDog(x) → hasFourLegs(x)), ∃x (isCat(x) ∧ isBlack(x)), ∀x (isPerson(x) → ∃y (isDog(y) ∧ owns(x, y))), ∀x ∀y ((isParent(x, y) ∧ isMale(x)) → isFather(x, y)), ∃x (isHuman(x) ∧ loves(x, Mary)),∀x (isStudent(x) ∧ studiesHard(x) → getsGoodGrades(x))
,∀x (isAnimal(x) → (∃y (isFood(y) ∧ eats(x, y))))
).
Then, by using the first-order logic constraint(s), write a function that determines which branch a log belongs to.

# Guidelines
- You MUST use the function signature `def is_branch_a(log: str) -> bool`.
- DO NOT output any code that is not related to the function, such as test cases.
"""

FLOW_CONSTRAINT_FEEDBACK = """
Your code failed {fails} test cases. Please try again.

{reasons}
"""

####################################
# Commonsense constraint
####################################

COMMONSENSE_CONSTRAINT_SYSTEM = """
# Identity
You are a software engineer that is extremely good at understanding business logic and user requirements.
You are responsible for writing functions to validate the correctness and usefulness of input data.
At each turn, you should first provide your step-by-step thinking for solving the task. Your thought process should be enclosed using "<thought>" tag.
After that, you should use write a function in a block of Python code to solve the task.
"""

COMMONSENSE_CONSTRAINT_USER = """
# Task
This is a class with multiple fields:

{class_definition}

Instances of this class can be found in these logs:

{logs}

Based on the logs, infer the valid values for each field by referencing these common types of data validation:
1. Data Type Check: can the string value be converted to a correct data type? (e.g., "0.0" -> float 0.0)
2. Code Check: does the value fall within a valid list of values? (e.g., postal codes, country codes, NAICS industry codes)
3. Range Check: does the value fall within a logical numerical range? (e.g., temperature, latitude, price).
4. Format Check: does the value follow a predefined format? (e.g., UUID, email).
5. Consistency Check: are two or more values logically consistent with each other? (e.g., delivery date must be after shipping date).
6. Presence Check: an important field shouldn't be left blank (e.g., userID).
7. Vulunerablity Check: Ensure strings are not vulnerable to injection type attacks (XSS, log4j, SQL injection, etc.).

Then, write a function that determines if a value is valid for all the fields.

# Guidelines
- You CAN use existing formats like UUIDs and ISO standards.
- You CAN use Python regex library by importing it.
- You MUST treat an object instance as a dict in your function. 
- You MUST use the function signature `def is_valid(instance: dict) -> bool`.
- You SHOULD return True if all checks passed, otherwise, raise Error on the specific violation with a detailed message.
- DO NOT output any code that is not related to the function, such as test cases.
"""

COMMONSENSE_CONSTRAINT_FEEDBACK = """
Your code failed {fails} test cases. Please try again.

{reasons}
"""


