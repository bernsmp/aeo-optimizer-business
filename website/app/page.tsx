import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Hero from '@/components/sections/Hero';
import FeaturedResources from '@/components/sections/FeaturedResources';
import EmailList from '@/components/sections/EmailList';
import ResourceCategories from '@/components/sections/ResourceCategories';
import FAQSection from '@/components/sections/FAQ';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main>
        <Hero />
        <FeaturedResources />
        <EmailList />
        <ResourceCategories />
        <FAQSection />
      </main>
      <Footer />
    </div>
  );
}
