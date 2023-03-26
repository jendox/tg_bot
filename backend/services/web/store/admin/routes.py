import typing

if typing.TYPE_CHECKING:
    from backend.services.web.app import Application


def setup_routes(app: "Application"):
    from backend.services.web.store.admin.views import AdminLoginView, AdminCurrentView, AdminLogoutView

    app.router.add_view("/admin.login", AdminLoginView)
    app.router.add_view("/admin.current", AdminCurrentView)
    app.router.add_view("/admin.logout", AdminLogoutView)
