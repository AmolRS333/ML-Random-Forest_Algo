import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, mean_absolute_error, mean_squared_error, r2_score,
    roc_curve, auc
)
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from typing import Dict, Any, Tuple, List

class MLProcessor:
    def __init__(self, df: pd.DataFrame, target_column: str):
        self.df = df
        self.target_column = target_column
        self.X = df.drop(columns=[target_column])
        self.y = df[target_column]
        self.is_classification = self._determine_problem_type()
        self.model = None
        self.metrics = {}
        self.plots = {}
        
    def _determine_problem_type(self) -> bool:
        """Determine if the problem is classification or regression."""
        unique_values = self.y.nunique()
        return unique_values < len(self.y) * 0.1  # Classification if less than 10% unique values 
        
    def _train_model(self) -> None:
        """Train the appropriate Random Forest model."""
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        if self.is_classification:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test
        
    def _calculate_metrics(self) -> None:
        """Calculate appropriate metrics based on problem type."""
        y_pred = self.model.predict(self.X_test)
        
        if self.is_classification:
            self.metrics = {
                'accuracy': accuracy_score(self.y_test, y_pred),
                'precision': precision_score(self.y_test, y_pred, average='weighted'),
                'recall': recall_score(self.y_test, y_pred, average='weighted'),
                'f1_score': f1_score(self.y_test, y_pred, average='weighted')
            }
        else:
            self.metrics = {
                'mae': mean_absolute_error(self.y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_pred)),
                'mse' : mean_squared_error(self.y_test, y_pred),
                'r2_score': r2_score(self.y_test, y_pred)
            }
            
    def _generate_plots(self) -> None:
        """Generate relevant plots based on problem type."""
        if self.is_classification:
            self._plot_confusion_matrix()
            self._plot_roc_curve()
        self._plot_feature_importance()
        
    def _plot_confusion_matrix(self) -> None:
        """Generate and store confusion matrix plot."""
        y_pred = self.model.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        self._save_plot('confusion_matrix')
        
    def _plot_roc_curve(self) -> None:
        """Generate and store ROC curve plot."""
        y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(10, 8))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        
        self._save_plot('roc_curve')
        
    def _plot_feature_importance(self) -> None:
        """Generate and store feature importance plot."""
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(12, 8))
        plt.title('Feature Importances')
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), self.X.columns[indices], rotation=45, ha='right')
        plt.tight_layout()
        
        self._save_plot('feature_importance')
        
    def _save_plot(self, plot_name: str) -> None:
        """Save plot to base64 string."""
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        self.plots[plot_name] = base64.b64encode(image_png).decode()
        
    def analyze(self) -> Dict[str, Any]:
        """Run the complete analysis pipeline."""
        self._train_model()
        self._calculate_metrics()
        self._generate_plots()
        
        return {
            'problem_type': 'classification' if self.is_classification else 'regression',
            'metrics': self.metrics,
            'plots': self.plots,
            'feature_importances': dict(zip(self.X.columns, self.model.feature_importances_))
        } 