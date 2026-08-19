from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., Laptop, Monitor, Server
    assigned_user = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # In Use, In Repair, Decommissioned
    ip_address = db.Column(db.String(45), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'device_name': self.device_name,
            'category': self.category,
            'assigned_user': self.assigned_user,
            'status': self.status,
            'ip_address': self.ip_address
        }

# Create Database Tables
with app.app_context():
    db.create_all()

# Route: Serve Dashboard
@app.route('/')
def index():
    return render_template('index.html')

# API Route: Get All Assets
@app.route('/api/assets', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    return jsonify([asset.to_dict() for asset in assets])

# API Route: Add New Asset
@app.route('/api/assets', methods=['POST'])
def add_asset():
    data = request.get_json()
    new_asset = Asset(
        device_name=data['device_name'],
        category=data['category'],
        assigned_user=data['assigned_user'],
        status=data['status'],
        ip_address=data.get('ip_address', 'N/A')
    )
    db.session.add(new_asset)
    db.session.commit()
    return jsonify({'message': 'Asset added successfully', 'asset': new_asset.to_dict()}), 201

# API Route: Update Asset
@app.route('/api/assets/<int:id>', methods=['PUT'])
def update_asset(id):
    asset = Asset.query.get_or_404(id)
    data = request.get_json()
    
    asset.device_name = data.get('device_name', asset.device_name)
    asset.category = data.get('category', asset.category)
    asset.assigned_user = data.get('assigned_user', asset.assigned_user)
    asset.status = data.get('status', asset.status)
    asset.ip_address = data.get('ip_address', asset.ip_address)
    
    db.session.commit()
    return jsonify({'message': 'Asset updated successfully', 'asset': asset.to_dict()})

# API Route: Delete Asset
@app.route('/api/assets/<int:id>', methods=['DELETE'])
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Asset deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)