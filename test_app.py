import unittest
from app import app, load_timetable, save_timetable

class TimetableTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        self.app = app.test_client()
        self.app.testing = True
        # Use a fake user session
        with self.app.session_transaction() as sess:
            sess['user'] = 'testuser'
        # Start with a clean timetable
        save_timetable('testuser', {})

    def test_add_activity(self):
        response = self.app.post('/add', data={
            'time': '9 am',
            'day': 'Monday',
            'activity': 'Math Class'
        }, follow_redirects=True)
        timetable = load_timetable('testuser')
        self.assertIn('9 am', timetable)
        self.assertEqual(timetable['9 am']['Monday'], 'Math Class')

    def test_edit_activity(self):
        save_timetable('testuser', {'9 am': {'Monday': 'Math Class'}})
        response = self.app.post('/edit/9 am/Monday', data={
            'activity': 'Science Class'
        }, follow_redirects=True)
        timetable = load_timetable('testuser')
        self.assertEqual(timetable['9 am']['Monday'], 'Science Class')

    def test_delete_activity(self):
        save_timetable('testuser', {'9 am': {'Monday': 'Math Class'}})
        response = self.app.post('/delete/9 am/Monday', follow_redirects=True)
        timetable = load_timetable('testuser')
        self.assertNotIn('Monday', timetable.get('9 am', {}))

if __name__ == '__main__':
    unittest.main()
