# generate_enhanced_vanet_dataset.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class VANETDatasetGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        # Vehicle pool
        self.vehicle_ids = [1000 + i for i in range(100)]
        
        # Define realistic ranges based on your data
        self.config = {
            'lat_range': (35.0, 35.5),
            'lon_range': (-119.5, -120.0),
            'speed_range': (30, 85),  # km/h
            'signal_range': (-95, -45),  # dBm
            'rsu_distance_range': (50, 500),
            'packet_loss_normal': (0.0, 0.1),
            'packet_loss_attack': (0.1, 0.95),
            'latency_normal': (15, 60),
            'latency_attack': (60, 85),
        }
        
        # Attack patterns configuration
        self.attack_patterns = {
            0: {'name': 'Normal', 'weight': 0.70},
            1: {'name': 'Sybil', 'weight': 0.08},
            2: {'name': 'DoS', 'weight': 0.07},
            3: {'name': 'FalseData', 'weight': 0.07},
            'Malware': {'name': 'Malware', 'weight': 0.05},
            'Eavesdropping': {'name': 'Eavesdropping', 'weight': 0.03}
        }
        
    def generate_normal_traffic(self, timestamp, vehicle_id):
        """Generate normal traffic patterns"""
        return {
            'vehicle_id': vehicle_id,
            'timestamp': timestamp,
            'latitude': np.random.uniform(*self.config['lat_range']),
            'longitude': np.random.uniform(*self.config['lon_range']),
            'speed': np.random.uniform(30, 75),
            'acceleration': np.random.uniform(-2, 2),
            'direction': np.random.uniform(0, 360),
            'lane_id': np.random.choice([1, 2, 3, 4]),
            'packet_loss_rate': np.random.uniform(0, 0.2),
            'signal_strength': np.random.uniform(-75, -50),
            'message_frequency': np.random.choice([5, 10, 50]),
            'data_volume': np.random.uniform(60, 120),
            'latency': np.random.uniform(15, 50),
            'weather_condition': np.random.choice(['sunny', 'rainy', 'foggy']),
            'traffic_density': np.random.randint(10, 100),
            'road_type': np.random.choice(['highway', 'urban'], p=[0.6, 0.4]),
            'RSU_distance': np.random.uniform(50, 400),
            'threat_type': 0
        }
    
    def generate_sybil_attack(self, timestamp, vehicle_id, cluster_center=None):
        """
        Sybil Attack Pattern:
        - Multiple IDs from similar location (clustered positions)
        - Similar signal strength patterns
        - Synchronized timing
        - Low hop counts
        """
        if cluster_center is None:
            cluster_center = {
                'lat': np.random.uniform(*self.config['lat_range']),
                'lon': np.random.uniform(*self.config['lon_range'])
            }
        
        data = self.generate_normal_traffic(timestamp, vehicle_id)
        
        # Sybil characteristics
        data['latitude'] = cluster_center['lat'] + np.random.uniform(-0.001, 0.001)
        data['longitude'] = cluster_center['lon'] + np.random.uniform(-0.001, 0.001)
        data['signal_strength'] = np.random.uniform(-65, -55)  # Similar signal
        data['packet_loss_rate'] = np.random.uniform(0.1, 0.2)
        data['message_frequency'] = 10  # Consistent frequency
        data['latency'] = np.random.uniform(30, 40)  # Similar latency
        data['RSU_distance'] = np.random.uniform(200, 250)  # Similar distance
        data['threat_type'] = 1
        
        return data
    
    def generate_dos_attack(self, timestamp, vehicle_id):
        """
        DoS Attack Pattern:
        - Extremely high message frequency
        - Large data volumes
        - High packet loss rate
        - Increased latency for all nodes
        """
        data = self.generate_normal_traffic(timestamp, vehicle_id)
        
        # DoS characteristics
        data['message_frequency'] = 50  # Flooding
        data['data_volume'] = np.random.uniform(130, 150)  # Large packets
        data['packet_loss_rate'] = np.random.uniform(0.8, 0.95)  # Network congestion
        data['latency'] = np.random.uniform(70, 85)  # High latency
        data['signal_strength'] = np.random.uniform(-70, -60)
        data['threat_type'] = 2
        
        return data
    
    def generate_false_data_attack(self, timestamp, vehicle_id):
        """
        False Data Injection Pattern:
        - Impossible speeds or positions
        - Inconsistent movement patterns
        - Abnormal acceleration values
        - Position outside road boundaries
        """
        data = self.generate_normal_traffic(timestamp, vehicle_id)
        
        attack_type = np.random.choice(['speed', 'position', 'acceleration'])
        
        if attack_type == 'speed':
            data['speed'] = np.random.uniform(150, 300)  # Impossible speeds
            data['acceleration'] = np.random.uniform(-8, 8)  # Extreme acceleration
        elif attack_type == 'position':
            data['latitude'] = np.random.uniform(34.5, 35.8)  # Out of normal range
            data['longitude'] = np.random.uniform(-118.5, -120.5)
        else:
            data['acceleration'] = np.random.uniform(-10, 10)  # Impossible acceleration
            data['direction'] = np.random.uniform(0, 360)
        
        data['packet_loss_rate'] = np.random.uniform(0.2, 0.3)
        data['threat_type'] = 3
        
        return data
    
    def generate_malware_pattern(self, timestamp, vehicle_id):
        """
        Malware Propagation Pattern:
        - Increased data volume (payload)
        - Multiple hop counts
        - Irregular message frequencies
        - Spreading pattern over time
        """
        data = self.generate_normal_traffic(timestamp, vehicle_id)
        
        data['data_volume'] = np.random.uniform(100, 140)  # Larger for payload
        data['message_frequency'] = np.random.choice([5, 10, 50])  # Irregular
        data['packet_loss_rate'] = np.random.uniform(0.1, 0.3)
        data['latency'] = np.random.uniform(40, 70)
        data['signal_strength'] = np.random.uniform(-75, -60)
        # Simulate spreading pattern
        data['RSU_distance'] = np.random.uniform(100, 500)
        data['threat_type'] = 'Malware'
        
        return data
    
    def generate_eavesdropping_pattern(self, timestamp, vehicle_id):
        """
        Eavesdropping Pattern:
        - Lower message frequency (passive listening)
        - Normal appearing metrics
        - Slightly weaker signal (distance)
        - Longer presence duration
        """
        data = self.generate_normal_traffic(timestamp, vehicle_id)
        
        data['message_frequency'] = 5  # Less active
        data['data_volume'] = np.random.uniform(50, 80)  # Lower volume
        data['signal_strength'] = np.random.uniform(-85, -70)  # Weaker signal
        data['packet_loss_rate'] = np.random.uniform(0, 0.15)
        data['latency'] = np.random.uniform(25, 45)
        data['threat_type'] = 'Eavesdropping'
        
        return data
    
    def generate_temporal_attack_sequence(self, start_time, attack_type, duration_ms=5000, num_vehicles=5):
        """
        Generate realistic temporal attack sequences
        - Attacks have temporal correlation
        - Multiple vehicles may be involved
        - Attacks have ramp-up and ramp-down phases
        """
        sequence = []
        attack_vehicles = np.random.choice(self.vehicle_ids, num_vehicles, replace=False)
        
        # Shared parameters for coordinated attacks
        cluster_center = None
        if attack_type == 1:  # Sybil
            cluster_center = {
                'lat': np.random.uniform(*self.config['lat_range']),
                'lon': np.random.uniform(*self.config['lon_range'])
            }
        
        for i in range(0, duration_ms, 100):  # 100ms intervals
            timestamp = start_time + timedelta(milliseconds=i)
            
            for vehicle_id in attack_vehicles:
                # Ramp-up phase
                if i < 1000:
                    intensity = i / 1000
                # Sustained attack
                elif i < duration_ms - 1000:
                    intensity = 1.0
                # Ramp-down phase
                else:
                    intensity = (duration_ms - i) / 1000
                
                if np.random.random() < intensity:
                    if attack_type == 1:
                        data = self.generate_sybil_attack(timestamp, vehicle_id, cluster_center)
                    elif attack_type == 2:
                        data = self.generate_dos_attack(timestamp, vehicle_id)
                    elif attack_type == 3:
                        data = self.generate_false_data_attack(timestamp, vehicle_id)
                    else:
                        data = self.generate_normal_traffic(timestamp, vehicle_id)
                    
                    sequence.append(data)
        
        return sequence
    
    def generate_dataset(self, n_samples=10000, attack_ratio=0.3):
        """
        Generate complete dataset with realistic attack distributions
        """
        data = []
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        current_time = start_time
        
        # Calculate samples per attack type
        n_attacks = int(n_samples * attack_ratio)
        n_normal = n_samples - n_attacks
        
        # Generate normal traffic
        for i in range(n_normal):
            current_time += timedelta(milliseconds=100)
            vehicle_id = np.random.choice(self.vehicle_ids)
            data.append(self.generate_normal_traffic(current_time, vehicle_id))
        
        # Generate attack sequences
        attacks_generated = 0
        while attacks_generated < n_attacks:
            attack_type = np.random.choice([1, 2, 3])
            duration = np.random.randint(2000, 10000)  # 2-10 seconds
            num_vehicles = np.random.randint(1, 6)
            
            sequence = self.generate_temporal_attack_sequence(
                current_time, attack_type, duration, num_vehicles
            )
            
            data.extend(sequence)
            attacks_generated += len(sequence)
            current_time += timedelta(milliseconds=duration)
        
        # Shuffle to mix attacks with normal traffic
        random.shuffle(data)
        
        # Sort by timestamp for temporal consistency
        data = sorted(data, key=lambda x: x['timestamp'])
        
        return pd.DataFrame(data[:n_samples])
    
    def add_network_effects(self, df):
        """
        Add network-wide effects of attacks
        When DoS occurs, affect nearby vehicles
        """
        dos_indices = df[df['threat_type'] == 2].index
        
        for idx in dos_indices:
            # Affect vehicles in temporal proximity
            time_window = 1000  # 1 second
            start_idx = max(0, idx - 10)
            end_idx = min(len(df), idx + 10)
            
            for i in range(start_idx, end_idx):
                if df.loc[i, 'threat_type'] == 0:  # Normal traffic
                    # Increase latency and packet loss for nearby normal traffic
                    df.loc[i, 'latency'] *= 1.5
                    df.loc[i, 'packet_loss_rate'] = min(0.95, df.loc[i, 'packet_loss_rate'] * 2)
        
        return df
    
    def generate_advanced_dataset(self, n_samples=10000):
        """
        Generate dataset with advanced attack patterns and network effects
        """
        print(f"Generating VANET dataset with {n_samples} samples...")
        
        # Generate base dataset
        df = self.generate_dataset(n_samples, attack_ratio=0.3)
        
        # Add network-wide effects
        df = self.add_network_effects(df)
        
        # Add derived features
        df['speed_variance'] = df.groupby('vehicle_id')['speed'].transform(
            lambda x: x.rolling(window=5, min_periods=1).std()
        )
        
        df['position_change_rate'] = df.groupby('vehicle_id').apply(
            lambda x: np.sqrt(
                x['latitude'].diff()**2 + x['longitude'].diff()**2
            ) / 0.1  # per 100ms
        ).reset_index(level=0, drop=True)
        
        # Add message integrity check (simulated)
        df['message_integrity'] = np.where(
            df['threat_type'].isin([3, 'FalseData']), 
            'Failed', 
            'Passed'
        )
        
        return df

def main():
    # Initialize generator
    generator = VANETDatasetGenerator(seed=42)
    
    # Generate dataset
    df = generator.generate_advanced_dataset(n_samples=10000)
    
    # Save to CSV
    output_file = 'enhanced_vanet_dataset.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\nDataset saved to '{output_file}'")
    print(f"Shape: {df.shape}")
    print(f"\nThreat distribution:")
    print(df['threat_type'].value_counts())
    
    print(f"\nDataset statistics:")
    print(df.describe())
    
    print(f"\nSample of attack patterns:")
    attack_samples = df[df['threat_type'] != 0].head(10)
    print(attack_samples[['timestamp', 'vehicle_id', 'threat_type', 'packet_loss_rate', 'latency']])
    
    # Analyze temporal patterns
    print(f"\nTemporal attack clustering:")
    attacks = df[df['threat_type'] != 0]
    if len(attacks) > 0:
        attacks['time_diff'] = attacks['timestamp'].diff().dt.total_seconds()
        clustered_attacks = attacks[attacks['time_diff'] < 1].shape[0]
        print(f"Clustered attacks (within 1 sec): {clustered_attacks}/{len(attacks)} ({100*clustered_attacks/len(attacks):.1f}%)")
    
    return df

if __name__ == "__main__":
    df = main()