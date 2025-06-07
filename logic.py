# This file will house the propositional logic engine and related data structures
# for the Propositional RPG. It will define how propositions are represented,
# stored, and manipulated.

# --- Logical Connectives ---
# These constants represent logical connectives that can be used to form
# complex propositions and rules.
IMPLIES = 'implies'
NOT = 'not'
OR = 'or'
AND = 'and'
# These constants will be used in logic rule functions to construct and match
# proposition patterns.

# --- Proposition Representation ---
# Propositions are represented as tuples. This structure allows for
# nested propositions, making it possible to represent complex statements
# such as one character knowing something about another character or object.

# Examples of propositions:

# Example 1: ('at', 'player', 'location_A')
#   - Predicate: 'at'
#   - Argument 1: 'player' (the character or object)
#   - Argument 2: 'location_A' (the location)
#   - Meaning: The player is at Location A.

# Example 2: ('knows', 'npc1', ('at', 'player', 'location_A'))
#   - Predicate: 'knows'
#   - Argument 1: 'npc1' (the character who knows)
#   - Argument 2: ('at', 'player', 'location_A') (the proposition that npc1 knows)
#   - Meaning: NPC1 knows that the Player is at Location A.
#   - Note: The third element is itself a proposition.

# Example 3: ('mood', 'npc1', 'angry')
#   - Predicate: 'mood'
#   - Argument 1: 'npc1' (the character)
#   - Argument 2: 'angry' (the state of the mood)
#   - Meaning: NPC1 is angry.

# Example 4: ('has_item', 'player', 'key')
#   - Predicate: 'has_item'
#   - Argument 1: 'player' (the character)
#   - Argument 2: 'key' (the item)
#   - Meaning: The Player has the key.

# Example 5: (IMPLIES, ('mood', 'npc1', 'angry'), ('action', 'npc1', 'shout'))
#   - Predicate: IMPLIES (logical connective)
#   - Argument 1: ('mood', 'npc1', 'angry') (antecedent proposition)
#   - Argument 2: ('action', 'npc1', 'shout') (consequent proposition)
#   - Meaning: If NPC1 is angry, then NPC1 will shout.

# Example 6: (AND, ('at', 'player', 'market'), ('has_item', 'player', 'gold'))
#   - Predicate: AND (logical connective)
#   - Argument 1: ('at', 'player', 'market')
#   - Argument 2: ('has_item', 'player', 'gold')
#   - Meaning: The player is at the market AND the player has gold.

# Example 7: (NOT, ('has_item', 'player', 'sword'))
#   - Predicate: NOT (logical connective)
#   - Argument 1: ('has_item', 'player', 'sword')
#   - Meaning: The player does NOT have a sword.


# --- Inference Rules ---

def modus_ponens(character_kb):
    """
    Applies Modus Ponens to a character's knowledge base.
    If the knowledge base contains (IMPLIES, P, Q) and P, then Q is inferred.

    Args:
        character_kb (set): A set of propositions representing the character's knowledge.

    Returns:
        list: A list of newly derived propositions. Returns an empty list if no new
              propositions are derived.

    Example:
        kb = {
            (IMPLIES, ('is_raining',), ('ground_is_wet',)),
            ('is_raining',),
            ('sky_is_blue',)
        }
        new_propositions = modus_ponens(kb)
        # new_propositions would be [('ground_is_wet',)]
        # kb would be updated to include ('ground_is_wet',)
    """
    newly_derived_propositions = []
    # Iterate over a copy of the set for safe checking, or collect implications first
    implications = [prop for prop in character_kb if isinstance(prop, tuple) and len(prop) == 3 and prop[0] == IMPLIES]

    for p_implies_q in implications:
        antecedent_p = p_implies_q[1]
        consequent_q = p_implies_q[2]

        if antecedent_p in character_kb:
            if consequent_q not in character_kb: # Avoid adding if already known
                newly_derived_propositions.append(consequent_q)

    if newly_derived_propositions:
        character_kb.update(newly_derived_propositions)

    return newly_derived_propositions

def modus_tollens(character_kb):
    """
    Applies Modus Tollens to a character's knowledge base.
    If the knowledge base contains (IMPLIES, P, Q) and (NOT, Q), then (NOT, P) is inferred.

    Args:
        character_kb (set): A set of propositions representing the character's knowledge.

    Returns:
        list: A list of newly derived propositions. Returns an empty list if no new
              propositions are derived.

    Example:
        kb = {
            (IMPLIES, ('has_wings', 'bird'), ('can_fly', 'bird')),
            (NOT, ('can_fly', 'bird')),
            ('is_animal', 'bird')
        }
        new_propositions = modus_tollens(kb)
        # new_propositions would be [(NOT, ('has_wings', 'bird'))]
        # kb would be updated to include (NOT, ('has_wings', 'bird'))
    """
    newly_derived_propositions = []
    implications = [prop for prop in character_kb if isinstance(prop, tuple) and len(prop) == 3 and prop[0] == IMPLIES]

    for p_implies_q in implications:
        antecedent_p = p_implies_q[1]
        consequent_q = p_implies_q[2]

        negation_of_consequent_q = (NOT, consequent_q)

        if negation_of_consequent_q in character_kb:
            negation_of_antecedent_p = (NOT, antecedent_p)
            if negation_of_antecedent_p not in character_kb: # Avoid adding if already known
                newly_derived_propositions.append(negation_of_antecedent_p)

    if newly_derived_propositions:
        character_kb.update(newly_derived_propositions)

    return newly_derived_propositions

def hypothetical_syllogism(character_kb):
    """
    Applies Hypothetical Syllogism to a character's knowledge base.
    If the KB contains (IMPLIES, P, Q) and (IMPLIES, Q, R), then (IMPLIES, P, R) is inferred.

    Args:
        character_kb (set): A set of propositions (tuples) representing the character's knowledge.

    Returns:
        list: A list of newly derived implication propositions. Returns an empty list
              if no new propositions are derived.

    Example:
        kb = {
            (IMPLIES, ('is_raining',), ('ground_is_wet',)),
            (IMPLIES, ('ground_is_wet',), ('worms_come_out',)),
            ('is_cloudy',)
        }
        new_implications = hypothetical_syllogism(kb)
        # new_implications would be [(IMPLIES, ('is_raining',), ('worms_come_out',))]
        # kb would be updated to include this new implication.
    """
    newly_derived_propositions = []
    implications = [prop for prop in character_kb if isinstance(prop, tuple) and len(prop) == 3 and prop[0] == IMPLIES]

    # Create a list of implications to iterate over to avoid issues with set modification if we were to add directly
    # However, we collect new propositions in a list first, so iterating over the filtered list is fine.

    for imp1 in implications:
        p = imp1[1]
        q1 = imp1[2] # This is the 'q' from (IMPLIES, p, q)

        for imp2 in implications:
            if imp1 == imp2: # Don't compare an implication with itself
                continue

            q2 = imp2[1] # This is the 'q_prime' from (IMPLIES, q_prime, r)
            r = imp2[2]

            if q1 == q2: # Check if the consequent of the first matches the antecedent of the second
                new_implication = (IMPLIES, p, r)
                if new_implication not in character_kb and new_implication not in newly_derived_propositions:
                    newly_derived_propositions.append(new_implication)

    if newly_derived_propositions:
        character_kb.update(newly_derived_propositions)

    return newly_derived_propositions

def conjunction(character_kb):
    """
    Applies Conjunction to a character's knowledge base.
    If the knowledge base contains P and Q, then (AND, P, Q) can be inferred.

    Args:
        character_kb (set): A set of propositions representing the character's knowledge.

    Returns:
        list: A list of newly derived conjunctions. Returns an empty list if no new
              conjunctions are derived.

    Example:
        kb = {('is_sunny',), ('is_warm',), ('is_windy',)}
        new_conjunctions = conjunction(kb)
        # new_conjunctions might include:
        #   (AND, ('is_sunny',), ('is_warm',))
        #   (AND, ('is_sunny',), ('is_windy',))
        #   (AND, ('is_warm',), ('is_windy',))
        # (assuming a consistent ordering for P and Q in (AND, P, Q))
        # kb would be updated to include these.
    """
    newly_derived_propositions = []
    propositions_list = list(character_kb)
    n = len(propositions_list)

    for i in range(n):
        for j in range(i + 1, n):
            p = propositions_list[i]
            q = propositions_list[j]

            # To ensure a canonical representation and avoid (AND, p, q) and (AND, q, p)
            # being treated differently if the KB doesn't already sort them,
            # we can sort p and q if they are strings, or rely on tuple comparison.
            # For simplicity here, we'll just form (AND, p, q) and (AND, q, p)
            # and let the set nature of character_kb handle duplicates if (AND,p,q) == (AND,q,p).
            # However, a more robust way is to ensure order.
            # Let's try to make p and q always be in a defined order.
            # A simple way: convert to string and compare, or use hash.
            # For tuples, standard tuple comparison works.

            # Ensure a canonical order for p and q within the AND proposition
            # This helps in consistently forming the conjunction and checking for existence.
            # If p and q are complex tuples, direct comparison works.
            prop1, prop2 = tuple(sorted((p, q), key=lambda x: str(x))) # Sort by string representation for consistency

            new_conj = (AND, prop1, prop2)

            if new_conj not in character_kb and new_conj not in newly_derived_propositions:
                newly_derived_propositions.append(new_conj)

    if newly_derived_propositions:
        character_kb.update(newly_derived_propositions)

    return newly_derived_propositions

def simplification(character_kb):
    """
    Applies Simplification to a character's knowledge base.
    If the knowledge base contains (AND, P, Q), then P is inferred and Q is inferred.

    Args:
        character_kb (set): A set of propositions representing the character's knowledge.

    Returns:
        list: A list of newly derived propositions. Returns an empty list if no new
              propositions are derived.

    Example:
        kb = {
            (AND, ('has_map', 'player'), ('has_compass', 'player')),
            ('has_boots', 'player')
        }
        # Assume ('has_map', 'player') is already in kb for this scenario variation
        # kb = {
        #     (AND, ('has_map', 'player'), ('has_compass', 'player')),
        #     ('has_boots', 'player'),
        #     ('has_map', 'player')
        # }
        new_propositions = simplification(kb)
        # If ('has_map', 'player') was already present and ('has_compass', 'player') was not:
        # new_propositions would be [('has_compass', 'player')]
        # If neither were present:
        # new_propositions would be [('has_map', 'player'), ('has_compass', 'player')]
        # kb would be updated to include both.
    """
    newly_derived_propositions = []
    conjunctions = [prop for prop in character_kb if isinstance(prop, tuple) and len(prop) == 3 and prop[0] == AND]

    for and_p_q in conjunctions:
        p = and_p_q[1]
        q = and_p_q[2]

        if p not in character_kb and p not in newly_derived_propositions:
            newly_derived_propositions.append(p)

        if q not in character_kb and q not in newly_derived_propositions:
            newly_derived_propositions.append(q)

    if newly_derived_propositions:
        character_kb.update(newly_derived_propositions)

    return newly_derived_propositions

def disjunctive_syllogism(character_kb):
    """
    Applies Disjunctive Syllogism to a character's knowledge base.
    If the knowledge base contains (OR, P, Q) and (NOT, P), then Q is inferred.
    If the knowledge base contains (OR, P, Q) and (NOT, Q), then P is inferred.

    Args:
        character_kb (set): A set of propositions representing the character's knowledge.

    Returns:
        list: A list of newly derived propositions. Returns an empty list if no new
              propositions are derived.

    Example 1:
        kb = {
            (OR, ('task_A_complete',), ('task_B_complete',)),
            (NOT, ('task_A_complete',))
        }
        new_propositions = disjunctive_syllogism(kb)
        # new_propositions would be [('task_B_complete',)]
        # kb would be updated to include ('task_B_complete',)

    Example 2:
        kb = {
            (OR, ('has_key', 'chest'), ('is_locked_pickable', 'chest')),
            (NOT, ('is_locked_pickable', 'chest'))
        }
        new_propositions = disjunctive_syllogism(kb)
        # new_propositions would be [('has_key', 'chest')]
        # kb would be updated to include ('has_key', 'chest')
    """
    newly_derived_propositions = []
    disjunctions = [prop for prop in character_kb if isinstance(prop, tuple) and len(prop) == 3 and prop[0] == OR]

    for or_p_q in disjunctions:
        p = or_p_q[1]
        q = or_p_q[2]

        negation_of_p = (NOT, p)
        negation_of_q = (NOT, q)

        if negation_of_p in character_kb:
            if q not in character_kb and q not in newly_derived_propositions:
                newly_derived_propositions.append(q)

        if negation_of_q in character_kb:
            if p not in character_kb and p not in newly_derived_propositions:
                newly_derived_propositions.append(p)

    if newly_derived_propositions:
        character_kb.update(newly_derived_propositions)

    return newly_derived_propositions

def addition(character_kb, p_to_check, q_to_add):
    """
    Applies Addition to a character's knowledge base.
    If the knowledge base contains P, then (OR, P, Q) can be inferred for any Q.
    The parameters p_to_check and q_to_add represent P and Q respectively.

    Args:
        character_kb (set): The character's knowledge base.
        p_to_check (tuple): The proposition that must exist in character_kb.
        q_to_add (tuple): The proposition to form the disjunction with.

    Returns:
        list: A list containing the new disjunction if it was added, otherwise an empty list.

    Example:
        kb = {('is_attacking_player',)}
        newly_added = addition(kb, ('is_attacking_player',), ('is_dangerous',))
        # newly_added would be [(OR, ('is_attacking_player',), ('is_dangerous',))] (or sorted)
        # kb would be updated to include this new disjunction.
        # If ('is_attacking_player',) was not in kb, newly_added would be [].
    """
    newly_derived_propositions = []
    if p_to_check in character_kb:
        # Ensure a canonical order for p_to_check and q_to_add within the OR proposition
        prop1, prop2 = tuple(sorted((p_to_check, q_to_add), key=lambda x: str(x)))

        new_disjunction = (OR, prop1, prop2)

        if new_disjunction not in character_kb:
            character_kb.add(new_disjunction) # Add directly as we are only adding one
            newly_derived_propositions.append(new_disjunction)

    return newly_derived_propositions

# --- Knowledge Base ---
# Each character (player and NPCs) will eventually have a "knowledge base" (KB).
# This KB will store the propositions that the character believes to be true.
# It could be implemented as a set or a list of propositions to allow for
# efficient lookup, addition, and removal of beliefs.
# For example:
# player_kb = {('at', 'player', 'start_area'), ('has_item', 'player', 'stick')}
# npc1_kb = {('mood', 'npc1', 'neutral'), ('knows', 'npc1', ('at', 'player', 'unknown'))}
