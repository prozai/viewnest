from app import create_app

app = create_app()

#import app.control.adminController as adminController
#import app.control.mainController as mainController

# Function to check if a blueprint is registered
def check_blueprint_registration(blueprint_name):
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(blueprint_name):
            return True
    return False

# Test if the blueprints are registered
blueprints_registered = {
    "loginBP": check_blueprint_registration("loginBP"),
    "propBP": check_blueprint_registration("propBP"),
    "adminBP": check_blueprint_registration("adminBP"),
    "buyerBP": check_blueprint_registration("buyerBP"),
}

# Print the registration status of each blueprint
for blueprint, is_registered in blueprints_registered.items():
    print(f"{blueprint}: {'Registered' if is_registered else 'Not Registered'}")

if __name__ == '__main__':
    app.run(debug=True)
