import Hero from '../components/Hero';
import { motion } from 'framer-motion';
import { HiMagnifyingGlass, HiChartBar, HiDevicePhoneMobile } from 'react-icons/hi2';

function Home() {
  const features = [
    {
      title: "Real-time Detection",
      desc: "Fast processing using optimized MobileNetV2 architecture.",
      icon: <HiMagnifyingGlass className="w-6 h-6 text-primary" />
    },
    {
      title: "High Accuracy",
      desc: "Trained on thousands of road damage samples for precision.",
      icon: <HiChartBar className="w-6 h-6 text-primary" />
    },
    {
      title: "Responsive Design",
      desc: "Works seamlessly on desktops, tablets, and smartphones.",
      icon: <HiDevicePhoneMobile className="w-6 h-6 text-primary" />
    }
  ];

  return (
    <div className="bg-background">
      <Hero />
      
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="p-8 rounded-3xl bg-slate-50 hover:bg-slate-100 transition-colors"
              >
                <div className="mb-4 inline-block p-3 bg-white rounded-2xl shadow-sm">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">{feature.title}</h3>
                <p className="text-slate-600 leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
