def create_session(app, username, password):
    with app.test_client() as client:
        response = client.post(
            '/login',
            json={
                'username': username,
                'password': password
            }
        )
        return response.json['session']
