def apply_differential_privacy(update, noise=0.1):
    if "contamination" in update:
        update["contamination"] += noise
    return update
