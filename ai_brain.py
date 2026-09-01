# ai_brain.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import warnings

# தேவையற்ற வார்னிங் மெசேஜ்களை மறைக்க
warnings.filterwarnings('ignore')

class JarvisAI:
    def __init__(self):
        # AI மாடல்: Random Forest (இது பல முடிவுகளை அலசி ஆராய்ந்து சரியானதைக் கணிக்கும்)
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        
    def predict_trend(self, historical_prices):
        """
        கடந்த கால விலைகளை வைத்து அடுத்து மார்க்கெட் ஏறுமா இறங்குமா என AI கணிக்கும்
        """
        # 1. டேட்டாவை AI-க்குப் புரியும் Pandas வடிவமாக மாற்றுவது
        df = pd.DataFrame(historical_prices, columns=['close'])
        
        # 2. Feature Engineering (மார்க்கெட்டின் ரகசியங்களைக் கணக்கிடுவது)
        df['SMA_3'] = df['close'].rolling(window=3).mean()
        df['SMA_7'] = df['close'].rolling(window=7).mean()
        df['Momentum'] = df['close'].pct_change()
        
        # 3. Target (அடுத்த கேண்டில் விலையை விட தற்போதைய விலை அதிகமாக இருந்தால் 1, இல்லையென்றால் 0)
        df['Target'] = (df['close'].shift(-1) > df['close']).astype(int)
        
        # காலியான டேட்டாவை நீக்குதல்
        df = df.dropna()
        
        # டேட்டா போதவில்லை என்றால் கணிக்க வேண்டாம்
        if len(df) < 10:
            return "HOLD", 0.0
            
        # 4. AI-க்கு ட்ரெயினிங் (Training the Brain)
        features = df[['SMA_3', 'SMA_7', 'Momentum']]
        target = df['Target']
        
        # பழைய டேட்டாவை வைத்து AI கற்றுக்கொள்கிறது
        self.model.fit(features[:-1], target[:-1])
        
        # 5. Prediction (தற்போதைய நிலையை வைத்து எதிர்காலத்தைக் கணிப்பது)
        current_state = features.iloc[-1:].values
        prediction = self.model.predict(current_state)
        confidence = self.model.predict_proba(current_state)[0].max() * 100
        
        if prediction[0] == 1:
            return "BUY", confidence
        else:
            return "SELL", confidence

# AI-ஐ ஆக்டிவேட் செய்ய ஒரு ஆப்ஜெக்ட்
brain = JarvisAI()