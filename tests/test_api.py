def test_internal_user_endpoint_returns_profile(client, app):
    from app.extensions import db
    from app.models import MemberProfile, User

    with app.app_context():
        user = User(
            auth_user_id=42,
            username='player-user',
            first_name='Player',
            last_name='One',
            display_name='Player One',
            email='player@example.com',
            platform_role='user',
            service_role='user',
            profile_complete=True,
        )
        db.session.add(user)
        db.session.flush()
        db.session.add(MemberProfile(user_id=user.id, first_name='Player', last_name='One', position='OL'))
        db.session.commit()

    response = client.get(
        '/api/internal/users/42',
        headers={'X-TT-Internal-Secret': 'test-internal-secret'},
    )
    payload = response.get_json()

    assert response.status_code == 200
    assert payload['user']['username'] == 'player-user'
    assert payload['user']['position'] == 'OL'
