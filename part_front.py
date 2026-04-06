def get_front_matter():
    return {
        "title": {
            "college": "[College Name]",
            "dept": "[Department Name]",
            "title": "Road Pothole and Damage Detection System\nUsing Deep Learning (CNN-MobileNetV2)",
            "degree": "Master of Computer Applications (MCA)",
            "student": "Neeraj Negi\nEnrollment No: [Enrollment Number]",
            "guide": "[Faculty Name]\n[Designation]",
            "year": "2025-26",
            "city": "[City, State]"
        },
        "certificate": "This is to certify that the Mini Project entitled \"Road Pothole and Damage Detection System Using Deep Learning\" is a bonafide work carried out by Neeraj Negi in partial fulfillment of MCA degree requirements.",
        "declaration": "I hereby declare that this Mini Project report titled \"Road Pothole and Damage Detection System Using Deep Learning\" is my own original work. It has not been submitted elsewhere for any degree or examination.",
        "acknowledgement": "I would like to express my sincere gratitude to my project guide, [Faculty Name], for their in-depth guidance, constant motivation, and constructive feedback throughout the lifecycle of this project. Their academic insights profoundly shaped the technical direction adopted in this study. I also extend my gratitude to the Head of Department, [HOD Name], for facilitating an environment conducive to research and innovation.\n\nFurthermore, I acknowledge [College Name] for tremendous institutional support and providing essential resources. My profound thanks go to the Sekilab Research Group (Japan) for openly publishing the RDD2022 dataset, accelerating worldwide research in intelligent transportation. Finally, I thank the vast open-source developer community, without whose dedicated work on frameworks like TensorFlow, React, and FastAPI, this rapid prototyping and robust system deployment would not be achievable.",
        "abstract": "The maintenance of vast road networks, such as India's 63 lakh kilometers, presents a substantial logistical and financial challenge that traditional manual visual inspection struggles to meet. Manual surveying is slow, expensive, inherently subjective, and exposes personnel to hazardous conditions. Consequently, delayed infrastructure repair frequently leads to severe accidents and exponentially higher rehabilitation costs. This project develops an automated, scalable, and cost-effective Road Pothole and Damage Detection System utilizing advanced deep learning methodologies.\n\nThe proposed solution features a highly efficient, dual-task Convolutional Neural Network (CNN) built upon the MobileNetV2 architecture. Engineered specifically for resource-constrained edge deployments, the model simultaneously executes image classification and pixel-level semantic segmentation. The system utilizes a substantial subset of the RDD2022 dataset, encompassing 19,892 diverse high-resolution images of Indian and Japanese road scenarios categorized into Normal, Crack, and Pothole surface classes. A customized two-stage transfer learning paradigm was deployed to navigate the hardware memory constraints of an NVIDIA RTX 2050 (4GB VRAM) while heavily optimizing model convergence through mixed precision computation.\n\nEmpirical evaluation confirms robust generalization, with the model achieving an overall validation accuracy of 84.74%. Notably, the model achieved a 100% recall rate for pothole identification, an essential criterion for preventative infrastructure safety. The system architecture incorporates a unique Repair Priority Score (RPS) to quantifiably assist in maintenance triage. The inference engine is modularly served through a FastAPI REST backend deployed on Hugging Face Spaces and interfaces seamlessly with an interactive React frontend hosted on Vercel, providing universal multi-platform access.\n\nKeywords: Deep Learning, CNN, MobileNetV2, Transfer Learning, Road Damage Detection, Image Classification, Semantic Segmentation",
        "lists": {
            "figures": [
                "Figure 1: System Architecture Overview", "Figure 2: MobileNetV2 Dual-Head Model Architecture",
                "Figure 3: Sample Images from RDD2022 Dataset", "Figure 4: Two-Stage Training Strategy",
                "Figure 5: Confusion Matrix", "Figure 6: Classification Confidence Bars (Dashboard Screenshot)",
                "Figure 7: Live Dashboard Screenshot \u2014 Pothole Detection", "Figure 8: Deployment Architecture Diagram"
            ],
            "tables": [
                "Table 1: Comparison of Existing Road Damage Detection Systems", "Table 2: Dataset Distribution (Normal, Crack, Pothole)",
                "Table 3: Model Hyperparameters and Configuration", "Table 4: Per-Class Evaluation Results",
                "Table 5: Comparison of Classification Metrics", "Table 6: Augmentation Techniques Applied"
            ]
        }
    }
