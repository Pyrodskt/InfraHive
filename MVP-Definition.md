Description du MVP

Définition de l'organisatioin (Tenant, Modules, DB, déploiement)
| Database
    | Shared (Général)
    | Premium => Database dédiée
    | Normal => Database shared | Schéma dédié
| Deployment/Running
    | Pour Premium, proxy en interne pour la collect d'information
| Tenants
    | Modules Management
    | Subscriptions Management

Modules Fonctionnel
PLATFORM
| Frontend (basic)
| API (basic)
| Auth
    | Local (email + password)
    | Identity Provider
        | Microsoft
| Automatisation 'new Tenant' / 'module managemet' (later - basic)

CMDB
| Inventory (Manuel et Auto)
    | Uniquement server et vm (pour le moment)
| Health Check
    | Policies
    | Intégration check
        | Agents
            | Integration
                | CheckMK
                | Rapid7
                | GLPI
                | Cortex XDR
        | Process (later [ex: via Agent])

Modules Technique
Inventory
| Manuel
| Automatique
    | Integration
        | ESX
        | Azure
        | AWS (later)
    | Agent (later)

Health Check
| Policies
| Integration
    | Agents
        | CheckMK
        | Rapid7
        | GLPI
        | Cortex XDR

Définition des Objets
USER
| email
| password_hashed
| first_name
| last_name

SERVER
| name
| hostname
| operating_system
| ip_address
| entity

TENANT