from core.api.permissions import CustomModelPermissions


class JobNotesPermissions(CustomModelPermissions):
    def __init__(self) -> None:
        self.perms_map["GET"] += ["jobs.view_job"]
