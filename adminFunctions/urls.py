









def add_roles_on_first_migrate():
    try:
        # Roles = getloop2.get_model('schema', 'Roles')
        default_roles_data = [{"id": 1, "role": "admin", "details": "an administration user"},
                              {"id": 2, "role": "user", "details": "a normal user"},
                              {"id": 3, "role": "agent", "details": "an agent user for any money exchange"}]
        Roles.objects.bulk_create(Roles(**values) for values in default_roles_data)
        if (Roles.objects.all().count()) == len(default_roles_data):
            print("All roles successfully added")
            return
        print("Some roles may not created please check")
    except Exception as e:
        print("Roles not created", e)