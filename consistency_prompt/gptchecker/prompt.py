####################################
# Input constraint
####################################

INPUT_CONSTRAINT_SYSTEM = """
# Identity
You are a software engineer that is extremely good at modelling entity relationships in databases.
You are responsible for checking how two different classes are related to each other.
At each turn, you should first provide your step-by-step thinking for solving the task. Your thought process should be enclosed using "<thought>" tag. 
After that, you should construct as many of the most important first-order logic constraints and output it in general format(eg: ∀x (isDog(x) → hasFourLegs(x))
, ∃x (isCat(x) ∧ isBlack(x)), ∀x (isPerson(x) → ∃y (isDog(y) ∧ owns(x, y))), ∀x ∀y ((isParent(x, y) ∧ isMale(x)) → isFather(x, y)), ∃x (isHuman(x) ∧ loves(x, Mary)),∀x (isStudent(x) ∧ studiesHard(x) → getsGoodGrades(x))
,∀x (isAnimal(x) → (∃y (isFood(y) ∧ eats(x, y))))
), then write a function in a block of Python code to solve the task based on the constraints and output all of them.
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
3. Matching: an attribute in an entity that must have the same value as an attribute in another entity, both attributes must be the same data type.

Then, write a function that determines if instances of [A] and [B] are related to each other using their attributes.

# Guidelines
- You MUST treat an object instance as a dict in your function. 
- You MUST use the function signature `def is_related(instance_A: dict, instance_B: dict) -> bool`.
- YOU MUST use all attributes of [A] and [B] in your functio for matching. If an attribute is not helpful for matching, simply check if it exists.
- DO NOT output any code that is not related to the function, such as test cases.
"""

INPUT_CONSTRAINT_FEEDBACK = """
Your code failed {fails} test cases. Please try again.

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
4. Format Check: does the value follow a predefined format? (e.g., UUID, email, phone number).
5. Consistency Check: are two or more values logically consistent with each other? (e.g., delivery date must be after shipping date).
6. Presence Check: an important field shouldn't be left blank (e.g., userID).
7. Length Check: does the value contain a correct number of characters? (e.g., password).

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