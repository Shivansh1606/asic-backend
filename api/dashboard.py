from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        # Statistics
        self.children.append(modules.LinkList(
            'Quick Links',
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                {
                    'title': 'View Website',
                    'url': 'http://localhost:3000',
                    'external': True,
                },
                {
                    'title': 'API Documentation',
                    'url': '/api/',
                    'external': False,
                },
            ],
            column=0,
            order=0
        ))

        # Recent Actions
        self.children.append(modules.RecentActions(
            'Recent Actions',
            10,
            column=0,
            order=1
        ))

        # Statistics
        self.children.append(modules.ModelList(
            'College Management',
            models=(
                'api.GalleryImage',
                'api.ManagementMember',
                'api.Staff',
                'api.Activity',
            ),
            column=1,
            order=0
        ))

        # Applications & Contacts
        self.children.append(modules.ModelList(
            'Applications & Contacts',
            models=(
                'api.StudentRegistration',
                'api.ContactSubmission',
                'api.UserProfile',
            ),
            column=2,
            order=0
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Application models',
            models=('*',),
            column=0,
            order=0
        ))
        
        self.children.append(modules.RecentActions(
            'Recent Actions',
            10,
            column=1,
            order=0
        ))
