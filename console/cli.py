def register_cli(app, repository):
    @app.cli.command('db_create')
    def db_create():
        repository.db.create_all()
        print('Database created!')

    @app.cli.command('db_drop')
    def db_drop():
        repository.db.drop_all()
        print('Database dropped!')


    @app.cli.command('db_seed')
    def db_seed():
        mercury = repository.planet(planet_name='Mercury',
                         planet_type='Class D',
                         home_star='Sol',
                         mass=2.258e23,
                         radius=1516,
                         distance=35.98e6)

        venus = repository.planet(planet_name='Venus',
                       planet_type='Class K',
                       home_star='Sol',
                       mass=4.867e24,
                       radius=3760,
                       distance=67.24e6)

        earth = repository.planet(planet_name='Earth',
                       planet_type='Class M',
                       home_star='Sol',
                       mass=5.972e24,
                       radius=3959,
                       distance=92.96e6)

        repository.db.session.add(mercury)
        repository.db.session.add(venus)
        repository.db.session.add(earth)

        test_user = repository.user(first_name='William',
                         last_name='Herschel',
                         email='test@test.com',
                         password='P@ssw0rd')

        repository.db.session.add(test_user)
        repository.db.session.commit()
        print('Database seeded!')


