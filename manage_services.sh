#!/bin/bash

# Service management script for Hacking Panel

case "$1" in
    start)
        echo "Starting Hacking Panel services..."
        systemctl start hackingpanel-backend
        systemctl start hackingpanel-frontend
        echo "Services started!"
        ;;
    stop)
        echo "Stopping Hacking Panel services..."
        systemctl stop hackingpanel-backend
        systemctl stop hackingpanel-frontend
        echo "Services stopped!"
        ;;
    restart)
        echo "Restarting Hacking Panel services..."
        systemctl restart hackingpanel-backend
        systemctl restart hackingpanel-frontend
        echo "Services restarted!"
        ;;
    status)
        echo "=== Backend Status ==="
        systemctl status hackingpanel-backend --no-pager -l
        echo ""
        echo "=== Frontend Status ==="
        systemctl status hackingpanel-frontend --no-pager -l
        ;;
    logs-backend)
        journalctl -u hackingpanel-backend -f
        ;;
    logs-frontend)
        journalctl -u hackingpanel-frontend -f
        ;;
    logs)
        journalctl -u hackingpanel-backend -u hackingpanel-frontend -f
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|logs-backend|logs-frontend}"
        echo ""
        echo "Commands:"
        echo "  start          - Start both services"
        echo "  stop           - Stop both services"
        echo "  restart        - Restart both services"
        echo "  status         - Show status of both services"
        echo "  logs           - View logs from both services (follow mode)"
        echo "  logs-backend   - View backend logs (follow mode)"
        echo "  logs-frontend  - View frontend logs (follow mode)"
        exit 1
        ;;
esac

