from cache import get_claims_sum

def proportional_rule(E, claims):
    """
    Proportional (PROP) rule: divides the estate proportionally to the claims.
    """
    total_claim = get_claims_sum(claims)
    if total_claim <= E:
        return list(claims)
    return [E * c / total_claim for c in claims]

def cea_rule(E, claims):
    """
    Constrained Equal Awards (CEA) rule: divides the estate equally among all agents, 
    up to their claim.
    """
    total_claim = get_claims_sum(claims)
    if total_claim <= E:
        return list(claims)
        
    n = len(claims)
    allocation = [0] * n
    remaining_E = E
    # Sort claims to process out the lower claims first
    sorted_claims = sorted([(c, i) for i, c in enumerate(claims)])
    
    for k, (c, i) in enumerate(sorted_claims):
        agents_left = n - k
        equal_share = remaining_E / agents_left
        award = min(c, equal_share)
        allocation[i] = award
        remaining_E -= award
        
    return allocation

def cel_rule(E, claims):
    """
    Constrained Equal Losses (CEL) rule: divides the total loss (sum of claims - E) 
    equally among agents, up to their claim amount.
    """
    total_claim = get_claims_sum(claims)
    if total_claim <= E:
        return list(claims)
        
    total_loss = total_claim - E
    n = len(claims)
    loss_allocation = [0] * n
    remaining_loss = total_loss
    sorted_claims = sorted([(c, i) for i, c in enumerate(claims)])
    
    for k, (c, i) in enumerate(sorted_claims):
        agents_left = n - k
        equal_loss_share = remaining_loss / agents_left
        loss = min(c, equal_loss_share)
        loss_allocation[i] = loss
        remaining_loss -= loss
        
    allocation = [claims[i] - loss_allocation[i] for i in range(n)]
    return allocation

def talmud_theta_rule(E, claims, theta=0.5):
    """
    Theta-Talmud rule (generalization of Talmud rule).
    If E <= sum(theta * c), applies CEA up to theta * c.
    If E > sum(theta * c), gives each agent their claim minus the CEA of the 
    remaining loss up to (1 - theta) * c.
    """
    total_claim = get_claims_sum(claims)
    theta_claims = [c * theta for c in claims]
    
    total_theta_claims = sum(theta_claims)
    if E <= total_theta_claims:
        return cea_rule(E, theta_claims)
    else:
        loss_to_divide = total_claim - E
        one_minus_theta_claims = [c * (1 - theta) for c in claims]
        loss_alloc = cea_rule(loss_to_divide, one_minus_theta_claims)
        return [c - l for c, l in zip(claims, loss_alloc)]

def talmud_rule(E, claims):
    """
    Talmud rule (Aumann and Maschler, 1985).
    This is a special case of the Theta-Talmud rule where theta = 0.5.
    """
    return talmud_theta_rule(E, claims, theta=0.5)

