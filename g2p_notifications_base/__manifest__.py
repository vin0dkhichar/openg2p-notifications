{
    "name": "G2P Notifications: Base",
    "category": "G2P",
    "version": "15.0.1.1.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "Other OSI approved licence",
    "development_status": "Production/Stable",
    "depends": [
        "g2p_programs",
    ],
    "data": [
        "views/email_notification_manager.xml",
        "views/sms_notification_manager.xml",
        "views/registrant.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_qweb": [],
    },
    "demo": [],
    "images": [],
    "application": False,
    "installable": True,
    "auto_install": False,
}
