DO
$$
    BEGIN
        CREATE TYPE user_role AS ENUM ('Администратор', 'Сотрудник', 'Гость');
    EXCEPTION
        WHEN duplicate_object THEN
            NULL;
    END
$$;