___all__ = ["stand_init", "crouch", "sit", "sit_relax", "stand", "stand_zero"]


def stand_init(motion_proxy, posture_proxy, tts_proxy):
    return posture_proxy.goToPosture("StandInit", 0.5)


def crouch(motion_proxy, posture_proxy, tts_proxy):
    return posture_proxy.goToPosture("Crouch", 0.5)


def sit(motion_proxy, posture_proxy, tts_proxy):
    return posture_proxy.goToPosture("Sit", 0.5)


def sit_relax(motion_proxy, posture_proxy, tts_proxy):
    return posture_proxy.goToPosture("SitRelax", 0.5)


def stand(motion_proxy, posture_proxy, tts_proxy):
    return posture_proxy.goToPosture("Stand", 0.5)


def stand_zero(motion_proxy, posture_proxy, tts_proxy):
    return posture_proxy.goToPosture("StandZero", 0.5)
