def roundRobin():
    config.round += 1
    if config.round == config.numServers - 1:
        return 0
    else:
        return config.round
