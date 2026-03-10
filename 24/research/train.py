import mlflow
import mlflow.sklearn
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import os

def main():
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("diabetes-prediction")
    
    diabetes = load_diabetes(scaled=False)
    X = diabetes.data
    y = diabetes.target
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Train samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    print(f"Features: {diabetes.feature_names}")
    
    with mlflow.start_run(run_name="random-forest-pipeline"):
        params = {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42
        }
        
        mlflow.log_params(params)
        
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor(**params))
        ])
        
        pipeline.fit(X_train, y_train)
        
        y_pred = pipeline.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)
        
        mlflow.sklearn.log_model(
            pipeline,
            "model",
            registered_model_name="diabetes"
        )
        
        run_id = mlflow.active_run().info.run_id
        
        print(f"\nRun ID: {run_id}")
        print(f"RMSE: {rmse:.2f}")
        print(f"R2 Score: {r2:.4f}")
    
    model_name = "diabetes"
    model_version = 1
    
    model_uri = f"models:/{model_name}/{model_version}"
    loaded_model = mlflow.sklearn.load_model(model_uri)
    
    print(f"\nModel loaded: {model_name} v{model_version}")
    
    test_sample = X_test[0:1]
    prediction = loaded_model.predict(test_sample)
    
    print(f"\nTest prediction:")
    print(f"Input: {test_sample[0]}")
    print(f"Prediction: {prediction[0]:.2f}")
    print(f"Actual: {y_test[0]:.2f}")
    
    os.makedirs("../model", exist_ok=True)
    mlflow.sklearn.save_model(loaded_model, "../model/diabetes_model")
    print("\nModel saved to ../model/diabetes_model")

if __name__ == "__main__":
    main()
