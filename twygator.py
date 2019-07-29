from app import app, db
from app.models import User, Friendship, Timeline_Member

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Friendship': Friendship, 'Timeline_Member': Timeline_Member}