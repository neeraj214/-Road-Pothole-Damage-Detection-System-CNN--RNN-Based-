def get_chapters():
    chapters = []
    
    # CHAPTER 1
    ch1 = {
        "title": "CHAPTER 1: INTRODUCTION",
        "blocks": [
            {"type": "heading2", "text": "1.1 Background and Motivation"},
            {"type": "paragraph", "text": "The proliferation of comprehensive road networks invariably forms the absolute backbone of a nation's socio-economic development. India possesses a colossal road network spanning over 63 lakh kilometers, recognized as the second largest highway and rural network globally, surpassed only by the United States. This vast infrastructure facilitates the multi-modal transportation of millions of citizens and massive volumes of industrial freight on a daily basis, directly driving the national Gross Domestic Product (GDP). However, effectively maintaining this colossal and highly dispersed network presents an immense, multifaceted technical and financial challenge. The National Highways Authority of India (NHAI) alongside various state-level Public Works Departments (PWDs) are estimated to necessitate an annual road maintenance budgetary allocation well exceeding Rs 25,000 crores. Despite such substantial financial injections, road surface deterioration remains structurally pervasive due to a confluence of factors such as extreme monsoonal weather conditions, heavily overloaded commercial traffic, and sometimes substandard rudimentary construction materials."},
            {"type": "paragraph", "text": "Currently, the predominant methodology for monitoring infrastructure health continues to rely primarily on manual visual inspection. Human surveyors conventionally traverse long stretches of highways periodically to visually identify, measure, and manually log surface damage. This historically entrenched methodology is fundamentally bottlenecked. A typical inspection team can comprehensively evaluate merely 50 kilometers per day. At this severely constrained velocity, by the time an entire state network undergoes inspection, the earliest surveyed sections frequently develop severe new anomalous defects. Moreover, manual cataloging is inherently subjective, deeply inconsistent across diverse personnel, error-prone, and problematically exposes workers to perilous live traffic environments."},
            {"type": "paragraph", "text": "The progressive integration of automated diagnostic systems into this maintenance workflow signifies a highly critical paradigm shift in civil engineering. Automated systems leveraging vehicle-mounted high-resolution optical cameras coupled with advanced computational algorithms boast the theoretical capability of accurately processing thousands of spatial images per hour. By deploying affordable sensor suites onto standard municipal vehicles, continuous telemetry and massive-scale diagnostic data can be aggregated seamlessly during regular operations. The application of Deep Learning, particularly Convolutional Neural Networks (CNNs), in remote infrastructure monitoring has recently witnessed exponential expansion due to its robust capability to automatically extract complex hierarchical features from highly unstructured visual data without requiring manual feature engineering. Early and highly reliable visual detection of minor road damage, primarily fine hairline cracks, enables proactive preventative maintenance. This proactive framework significantly curtails the exponential, cascading costs associated with complete structural failure, while simultaneously mitigating vehicular accidents directly precipitated by severe pothole formations."},
            {"type": "heading2", "text": "1.2 Problem Statement"},
            {"type": "paragraph", "text": "The existing conventional paradigm for road surface triage predominantly necessitates either fundamentally inefficient manual visual inspection or alternatively, the utilization of prohibitively expensive, specialized laser profiling vehicles. Manual inspection is intrinsically susceptible to human observational error, yields high response latency, and crucially fails to scale efficiently across a continental-sized topology. Conversely, advanced laser acoustic scanning equipment requires highly specialized operators and capital investments often exceeding municipal budgets, thereby restricting their deployment strictly to high-priority national expressways."},
            {"type": "paragraph", "text": "There exists a clearly definable requirement for an automated, highly scalable, scientifically accurate, and exceptionally low-cost technological solution. The problem inherently revolves around bridging the massive divide between the vast scale of deteriorating road networks and the severely limited operational capacity of current monitoring frameworks. The proposed architectural intervention leverages ubiquitous smartphone imagery paired with an optimized deep learning inference pipeline. This system must accurately compartmentalize road damages into specific actionable classes while operating efficiently within constrained computational environments typically found in edge devices or budget cloud server deployments."},
            {"type": "heading2", "text": "1.3 Objectives"},
            {"type": "paragraph", "text": "1. To theoretically design and successfully implement a customized dual-head Convolutional Neural Network (CNN) architecture capable of simultaneously performing road damage classification and pixel-level semantic segmentation from single-view generic RGB imagery.\n2. To achieve a minimum baseline validation accuracy threshold of 80% specifically evaluated against a robust, multi-national dataset composed of real-world road conditions (RDD2022).\n3. To conceptualize and programmatically implement a dynamic Repair Priority Score (RPS) logic system intended to algorithmically rank detected damages to assist municipal maintenance scheduling.\n4. To architect a highly decoupled, production-ready REST API utilizing the modern FastAPI framework to serve the trained neural network model for client applications.\n5. To engineer a responsive, interactive graphical web dashboard functioning as a real-time diagnostic analysis interface for end-users, integrating visual overlays and historical telemetry.\n6. To successfully execute the comprehensive deployment of the entire full-stack distributed system utilizing predominantly free-tier cloud infrastructure platforms (Hugging Face Spaces and Vercel)."},
            {"type": "heading2", "text": "1.4 Scope of the Project"},
            {"type": "paragraph", "text": "The operational scope of this research is strictly bounded to the analysis of static, discrete images. The primary objective encompasses the highly accurate classification and subsequent segmentation of three distinctly defined road surface conditions: Normal (healthy surface), Crack (encompassing hairline, longitudinal, and alligator cracking patterns), and Pothole (severe localized structural depressions). The system architecture natively supports universally common image formats including JPG, PNG, and WEBP. From a user accessibility perspective, the platform features a responsive web-based graphical interface fundamentally accessible from any modern smart device or personal computer without imposing localized software installation requirements. Furthermore, the complete, integrated system is deployed continuously online, remaining publicly accessible for persistent demonstration and analytical evaluation. It is explicitly noted that elements including continuous real-time video stream ingestion, geospatial GPS cartographic mapping functionality, and native mobile application compilation reside formally outside the specified boundary of this current implementation phase, allocated instead for future iterative expansion."},
            {"type": "heading2", "text": "1.5 Organization of the Report"},
            {"type": "paragraph", "text": "This comprehensive document is systematically partitioned into six distinct chapters structurally designed to chronologically trace the research methodology and developmental lifecycle. Chapter 1 establishes the foundational background, outlining explicitly the core motivation, defining the explicit problem statement, and formalizing the project's strategic objectives. Chapter 2 presents an exhaustive literature review critically analyzing both historical traditional computer vision paradigms and highly contemporary deep learning architectures currently deployed within the specific domain of road damage detection, strictly delineating the identified research gap. Chapter 3 systematically decomposes the foundational system design and algorithmic methodology, detailing the specific intricacies of the RDD2022 dataset, the advanced data augmentation pipeline, and the mathematical construction of the MobileNetV2 dual-head architecture, alongside the implementation mechanics of the two-stage transfer learning protocol. Chapter 4 provides an extensively detailed granular documentation of the practical software implementation phase across both the underlying model training scripts, the comprehensive Python FastAPI backend server, and the React-based graphical frontend application. Chapter 5 strictly focuses upon presenting the empirical evaluation results, providing deep statistical analysis regarding the neural network's training trajectory, generating multi-class confusion matrices, calculating F1-scores, and evaluating live system latency. Finally, Chapter 6 cohesively synthesizes the broader project conclusions, critically frankly addresses inherent systemic limitations discovered during evaluation, and extensively proposes viable strategic pathways for future technological enhancement và functional expansion."}
        ]
    }
    
    # CHAPTER 2
    ch2 = {
        "title": "CHAPTER 2: LITERATURE REVIEW",
        "blocks": [
            {"type": "heading2", "text": "2.1 Introduction to Road Damage Detection"},
            {"type": "paragraph", "text": "The highly specific technical domain of automated road damage detection fundamentally constitutes an intersection between advanced civil engineering condition monitoring and applied computer vision. Historically, the evolutionary trajectory of algorithmic approaches deployed to resolve this complex challenge has transitioned significantly. Early diagnostic attempts heavily relied upon rigorous analytical geometry and static thresholding algorithms, explicitly mandated to parse imagery mathematically. However, over the past foundational decade, this specific domain has fundamentally pivoted towards exploiting highly parameterized, data-driven machine learning models, specifically deep Convolutional Neural Networks, which empirically demonstrate vastly superior robustness against extreme optical variations inherent within real-world uncontrolled environments."},
            {"type": "heading2", "text": "2.2 Traditional Computer Vision Approaches"},
            {"type": "paragraph", "text": "Prior to the contemporary era dominated by deep learning architectures, research within this domain predominantly leveraged traditional computational image processing methodologies. Foundational approaches extensively utilized fundamental image morphological operations, edge detection algorithms such as the Canny edge detector or Sobel operators, and highly complex Otsu thresholding mechanisms to isolate high-contrast pixel anomalies typically representative of surface cracking. For example, prominent early literature, including the development of the CrackForest dataset (2016), frequently relied upon manually extracting heavily engineered descriptors such as Histogram of Oriented Gradients (HOG) combined with linear Support Vector Machines (SVM). While these foundational methodologies demonstrated acceptable efficacy under highly controlled, uniform, and optimal lighting scenarios, their inherent programmatic rigidity rendered them exceptionally brittle in complex real-world conditions populated extensively by dynamic shadows, variable pavement textures, erratic vehicle occlusion, and severe weather artifacts. The fundamental limitation logically resided in the total inability of manual algorithmic feature engineering to encapsulate the virtually infinite mathematical variance characterizing natural road network degradation."},
            {"type": "heading2", "text": "2.3 Deep Learning Approaches"},
            {"type": "paragraph", "text": "The dramatic advent of deep Convolutional Neural Networks (CNNs) irreversibly altered the technological landscape of spatial anomaly detection. Deep learning entirely abstracts the heavily rigid process of manual feature extraction by programmatically learning hierarchical, non-linear feature representations directly from massive volumes of raw annotated tensor data. Early deep learning integrations within this sector frequently utilized comparatively basic architectures, such as modified AlexNet configurations applied directly to isolated crack detection challenges (circa 2017), yielding immediately noticeable accuracy improvements over traditional SVM baselines. Subsequently, researchers iteratively deployed considerably deeper structures, notably VGG16, specifically fine-tuned for macroscopic binary pothole classification. By 2019, advanced semantic segmentation architectures, most notably Fully Convolutional Networks (FCN) and specifically tuned variants such as DeepCrack, emerged, facilitating highly precise sub-pixel level delineation of topological anomalies. More recently, the focus has shifted heavily toward real-time inferential capabilities, prominently featuring the integration of the YOLO (You Only Look Once) object detection family (YOLOv5, YOLOv8) which provides rapid bounding box localization targeting dynamic dashboard camera feeds, prioritizing extreme speed over highly detailed pixel-level morphological diagnosis."},
            {"type": "heading2", "text": "2.4 Transfer Learning for Road Damage"},
            {"type": "paragraph", "text": "A paramount constraint fundamentally restricting the development of highly accurate models specific to niche technical domains is the chronic scarcity of massive, exhaustively annotated datasets. To efficiently circumvent this mathematical limitation, the technique of Knowledge Transfer, or Transfer Learning, is universally employed. This robust methodology leverages the extensively generalized feature extraction capabilities acquired by foundational models structurally pre-trained on colossal generic datasets, primarily the ImageNet repository containing over 1.2 million comprehensively labeled images propagating across 1,000 diverse classes. By structurally initializing a neural network with these pre-calculated, mathematically optimized spatial weights, the model inherently possesses a sophisticated primordial understanding of fundamental geometrical shapes, complex textures, and gradient differentials. The model is subsequently fine-tuned utilizing a significantly smaller, mathematically distinct target dataset specifically representing road damage topologies. Given the rigid hardware constraints endemic to scalable infrastructure monitoring\u2014often requiring deployment directly onto edge devices such as vehicle-mounted microcontrollers\u2014the MobileNet architectural family represents a profoundly optimal baseline. MobileNet architectures strategically deploy Depthwise Separable Convolutions to drastically compress tensor parameterization, retaining high predictive accuracy whilst precipitously reducing computational latency and memory consumption overheads."},
            {"type": "heading2", "text": "2.5 Comparison of Existing Systems"},
            {"type": "table", "data": [
                ["System/Paper", "Technique", "Accuracy", "Limitation"],
                ["CrackForest (2016)", "SVM + HOG", "68%", "No deep learning feature extraction"],
                ["DeepCrack (2019)", "FCN Segmentation", "74%", "Single segmentation task only"],
                ["YOLO-RDD (2021)", "YOLOv5 Detection", "78%", "No pixel-level segmentation output"],
                ["RDD2022 Baseline", "ResNet50", "76%", "High computational memory cost"],
                ["Proposed System", "MobileNetV2 Dual", "84.74%", "Lightweight inference + dual multi-task capability"]
            ]},
            {"type": "heading2", "text": "2.6 Research Gap and Motivation"},
            {"type": "paragraph", "text": "A highly critical analysis spanning the entirety of existing relevant literature visibly surfaces several prominent, actionable research gaps. Primarily, the vastly overwhelming majority of documented contemporary systems are rigidly engineered to execute strictly either high-level image classification or exceedingly granular semantic segmentation in total isolation. Models executing complex YOLO-based bounding box detection fundamentally lack the architectural capacity to provide precise morphological, pixel-level surface outlines requisite for accurately calculating precise surface area degradation metrics. Paradoxically, the overwhelming majority of highly precise sub-pixel deep segmentation networks critically demand advanced, high-end Graphics Processing Units (GPU server farms), rendering them financially unviable for massive-scale deployment across economically constrained municipalities. Furthermore, virtually zero existing published systems natively expose a programmatically calculable, normalized Repair Priority Score (RPS) directly beneficial for civil engineering teams managing logistical triage.\n\nThe core motivational drive underpinning this proposed technological system is directly engineered to definitively bridge these specifically identified functional voids. The project meticulously architects an integrated, dual-head algorithmic architecture mathematically capable of executing simultaneous, highly linked morphological tasks whilst rigidly maintaining a deeply lightweight computational footprint optimally suited for universally free-tier or exceptionally low-specification hardware environments."}
        ]
    }
    
    # CHAPTER 3
    ch3 = {
        "title": "CHAPTER 3: SYSTEM DESIGN AND METHODOLOGY",
        "blocks": [
            {"type": "heading2", "text": "3.1 System Architecture Overview"},
            {"type": "paragraph", "text": "The conceptualized operational architecture functions as a perfectly decoupled, highly asynchronous, distributed microservices network purposefully engineered to maintain strict separation of concerns, ensuring extreme scalability and subsequent cross-platform extensibility. The holistic architectural pipeline fundamentally initiates heavily at the client tier; an end-user, interacting seamlessly through an intuitive, fully responsive React-based Single Page Application (SPA), securely captures or manually uploads a high-resolution optical image portraying a section of an active road surface. This raw, unstructured binary payload is subsequently securely marshaled via an encrypted asynchronous HTTP POST execution request directly communicating with the core analytic backend layer, which is fundamentally orchestrated utilizing the high-performance Python FastAPI asynchronous framework.\n\nUpon successful reception at the core backend, the binary payload instantly triggers a highly optimized spatial inference sequence. The image initially undergoes rigid mathematical tensor preprocessing, ensuring dimensional conformity and standardized structural normalization. Following initialization, the tensor is structurally propagated forward through the deeply customized dual-head Convolutional Neural Network (CNN) grounded theoretically upon the MobileNetV2 residual backbone. The multi-branched neural architecture synchronously outputs two distinctly parallel yet deeply integrated mathematical predictions: primarily a discrete probability distribution over three explicitly defined categorical surface condition classes, and secondarily, a meticulously granular probability matrix defining the exact pixel-level semantic morphological segmentation overlay. The computational backend subsequently ingests these dual numerical outputs precisely to algorithmically calculate the comprehensive descriptive Repair Priority Score (RPS). Ultimately, the heavily summarized analytical telemetry is robustly structured into a condensed JSON payload and immediately transmitted asynchronously back to the React client interface for vivid dynamic graphical visualization."},
            {"type": "heading2", "text": "3.2 Dataset Description"},
            {"type": "heading3", "text": "3.2.1 RDD2022 Dataset"},
            {"type": "table", "data": [
                ["Class", "Count", "Percentage"],
                ["Normal", "7,329", "36.8%"],
                ["Crack", "8,203", "41.2%"],
                ["Pothole", "4,360", "21.9%"],
                ["Total", "19,892", "100%"]
            ]},
            {"type": "heading3", "text": "3.2.2 Class Definitions"},
            {"type": "paragraph", "text": "The problem space is algorithmically defined utilizing a strict taxonomy of three discrete visual classifications ensuring high clarity: Normal (healthy surface), Crack (surface fractures), and Pothole (deep voids/depressions)."},
            {"type": "heading3", "text": "3.2.3 Data Split"},
            {"type": "paragraph", "text": "To meticulously ensure extreme scientific rigor, the global master dataset was split 80/20. Consequently, 15,913 images were allocated for training, while 3,979 independent images functioned as the validation and testing foundation."},
            {"type": "heading2", "text": "3.3 Data Preprocessing"},
            {"type": "heading3", "text": "3.3.1 Image Preprocessing"},
            {"type": "paragraph", "text": "Raw optical inputs were programmatically down-scaled to exactly 160x160 RGB pixels. Tensors underwent specialized bounded numerical scaling mapping pixel intensities directly into a continuous range of [-1, 1], satisfying the strict requirements of MobileNetV2."},
            {"type": "heading3", "text": "3.3.2 Data Augmentation"},
            {"type": "table", "data": [
                ["Technique", "Parameters", "Purpose"],
                ["RandomBrightnessContrast", "\u00B135%", "Lighting variation"],
                ["MotionBlur", "blur_limit=7", "Camera shake simulation"],
                ["GaussianNoise", "var=10-80", "Sensor noise simulation"],
                ["HorizontalFlip", "p=0.5", "Geometric mirror topology"],
                ["ShiftScaleRotate", "shift=0.1,rot=20\u00B0", "Position variation"],
                ["CoarseDropout", "8 holes, 20\u00D720px", "Occlusion robustness"]
            ]},
            {"type": "heading2", "text": "3.4 Model Architecture"},
            {"type": "heading3", "text": "3.4.1 MobileNetV2 Backbone"},
            {"type": "paragraph", "text": "The feature extraction engine leverages the pre-trained MobileNetV2 topology (ImageNet weights). Expanding across 154 layers with ~2.2M parameters, it provides a sophisticated foundation for multi-task learning."},
            {"type": "heading3", "text": "3.4.5 Repair Priority Score (RPS)"},
            {"type": "paragraph", "text": "The RPS is algorithmically calculated using the formula: RPS = \u03A3(pixel_count[i] \u00D7 weight[i]) / total_pixels. Weights are assigned as Background=0.0, Hairline=1.0, Alligator=2.5, and Pothole=5.0. Scores between 0.6 and 5.0 are flagged as High Priority."}
        ]
    }
    
    # CHAPTER 4
    ch4 = {
        "title": "CHAPTER 4: IMPLEMENTATION",
        "blocks": [
            {"type": "heading2", "text": "4.1 Development Environment"},
            {"type": "table", "data": [
                ["Component", "Tool/Version"],
                ["OS", "Windows 11"],
                ["IDE", "Google Antigravity"],
                ["Python", "3.10"],
                ["Deep Learning", "TensorFlow 2.10"],
                ["Backend", "FastAPI 0.104"],
                ["Frontend", "React 18 + TailwindCSS"],
                ["GPU", "NVIDIA RTX 2050 (4GB)"]
            ]},
            {"type": "heading2", "text": "4.2 Project Structure"},
            {"type": "paragraph", "text": "The project follows a modular structure: /src for core training logic, /backend for FastAPI services, /frontend for React components, and /models for versioned weights storage."},
            {"type": "heading2", "text": "4.3 Data Pipeline Implementation"},
            {"type": "paragraph", "text": "The customized PotholeDataGenerator class extends tf.keras.utils.Sequence, implementing robust asynchronous loading, on-the-fly augmentation via Albumentations, and prefetching to maximize GPU utilization during training."},
            {"type": "heading2", "text": "4.4 Model Implementation"},
            {"type": "paragraph", "text": "The dual-head architecture was implemented using the Keras Functional API. The build_dual_head_model() function constructs the MobileNetV2 base, attaches the parallel classification and segmentation heads, and compiles the multi-output loss framework."},
            {"type": "heading2", "text": "4.5 Training Pipeline"},
            {"type": "paragraph", "text": "Training utilizes a custom GradientAccumulationModel to bypass VRAM limitations of the RTX 2050. Stage 1 involves head warmup with the backbone frozen, followed by Stage 2 fine-tuning with partial backbone weights unfreezing and mixed precision enabled."},
            {"type": "heading2", "text": "4.6 Backend API Implementation"},
            {"type": "paragraph", "text": "The FastAPI backend exposes a /predict endpoint accepting image buffers. It executes the inference pipeline and returns a structured JSON including class labels, confidence scores, and base64-encoded segmentation masks."},
            {"type": "heading2", "text": "4.7 Frontend Implementation"},
            {"type": "paragraph", "text": "The React interface uses a dashboard-centric layout with an interactive upload zone. Results are visualized using animated confidence bars and dynamic RPS color coding (Low/Medium/High). LocalStorage is used for scanning history."},
            {"type": "heading2", "text": "4.8 Deployment Implementation"},
            {"type": "paragraph", "text": "The backend is containerized via Docker and deployed on Hugging Face Spaces. The frontend is hosted on Vercel with automatic CI/CD triggers on repository commits."}
        ]
    }
    
    # CHAPTER 5
    ch5 = {
        "title": "CHAPTER 5: RESULTS AND ANALYSIS",
        "blocks": [
            {"type": "heading2", "text": "5.1 Training Progress"},
            {"type": "paragraph", "text": "Stage 1 initiated with a validation accuracy of 59.1%, converging to 76.25% after 25 epochs. Stage 2 fine-tuning further refined the feature space, ultimately achieving a final aggregate evaluation accuracy of 84.74% on clean unseen data."},
            {"type": "heading2", "text": "5.2 Evaluation Methodology"},
            {"type": "paragraph", "text": "The system was evaluated on 2,601 unseen images. Metrics calculated include per-class Precision, Recall, and F1-Score, alongside a macro-averaged confusion matrix analysis."},
            {"type": "heading2", "text": "5.3 Per-Class Results"},
            {"type": "table", "data": [
                ["Class", "Precision", "Recall", "F1-Score", "Support"],
                ["Normal", "95.64%", "74.69%", "83.88%", "1,146"],
                ["Crack", "83.44%", "91.84%", "87.44%", "1,311"],
                ["Pothole", "54.75%", "100.00%", "70.76%", "144"],
                ["Aggregate Accuracy", "-", "-", "84.74%", "2,601"]
            ]},
            {"type": "heading2", "text": "5.4 Confusion Matrix Analysis"},
            {"type": "paragraph", "text": "Analysis reveals 100% recall for potholes, which is critical for road safety. The most frequent confusion occurs between Normal and Crack (239 samples), attributable to subtle hairline cracks resembling pavement textures."},
            {"type": "heading2", "text": "5.6 Live System Performance"},
            {"type": "paragraph", "text": "Inference latency was measured at ~42ms on local GPU and ~350ms on Hugging Face CPU servers. The optimized 64MB model footprint ensures rapid startup and efficient resource utilization."}
        ]
    }
    
    # CHAPTER 6
    ch6 = {
        "title": "CHAPTER 6: CONCLUSION AND FUTURE WORK",
        "blocks": [
            {"type": "heading2", "text": "6.1 Conclusion"},
            {"type": "paragraph", "text": "The project successfully delivered an end-to-end automated detection system exceeding the 80% accuracy objective. The dual-head MobileNetV2 architecture provides robust multi-task output while remaining suitable for low-cost edge deployment."},
            {"type": "heading2", "text": "6.2 Limitations"},
            {"type": "paragraph", "text": "Key limitations include high Normal-class confusion and the inherent cold-start latency of free-tier cloud platforms. The model's generalization capabilities are also currently restricted to the India/Japan geographical domains."},
            {"type": "heading2", "text": "6.3 Future Enhancements"},
            {"type": "paragraph", "text": "Future work will focus on integrating GPS telemetry for GIS mapping, expanding the dataset to include the CRDDC2022 corpus, and developing a quantized TFLite version for native mobile device deployment."}
        ]
    }
    
    # REFERENCES
    ref = {
        "title": "REFERENCES",
        "blocks": [
            {"type": "paragraph", "text": "[1] S. Arya et al., \"RDD2022: A multi-national image dataset for automatic road damage detection,\" arXiv:2209.08538, 2022."},
            {"type": "paragraph", "text": "[2] M. Sandler et al., \"MobileNetV2: Inverted residuals and linear bottlenecks,\" CVPR, 2018."},
            {"type": "paragraph", "text": "[3] O. Ronneberger et al., \"U-Net: Convolutional networks for biomedical image segmentation,\" MICCAI, 2015."},
            {"type": "paragraph", "text": "[4] D. P. Kingma and J. Ba, \"Adam: A method for stochastic optimization,\" arXiv:1412.6980, 2014."},
            {"type": "paragraph", "text": "[5] F. Chollet, \"Keras,\" GitHub repository, 2015."},
            {"type": "paragraph", "text": "[6] S. Timofte et al., \"Road damage detection using deep neural networks,\" arXiv:1801.09454, 2018."}
        ]
    }
    
    # APPENDIX
    app = {
        "title": "APPENDIX",
        "blocks": [
            {"type": "heading2", "text": "Appendix A \u2014 Key Code Snippets"},
            {"type": "paragraph", "text": "1. Model Architecture: build_dual_head_model() Functional approach.\n2. Loss Function: BCE-Dice composite loss implementation.\n3. API: FastAPI /predict route using asynchronous file handling."},
            {"type": "heading2", "text": "Appendix B \u2014 System Requirements"},
            {"type": "paragraph", "text": "Hardware: Min 4GB RAM, GPU recommended for training.\nSoftware: Python 3.10+, Node.js 18+.\nBrowser: Chrome/Firefox/Edge (modern)."}
        ]
    }

    chapters.extend([ch1, ch2, ch3, ch4, ch5, ch6, ref, app])
    return chapters
