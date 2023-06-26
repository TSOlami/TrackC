import { useState } from 'react';
import Profile from '../components/Profile';
import TopCryptoTable from '../components/TopCryptoTable';
import TransactionTable from '../components/TransactionTable';
import Header from '../components/Header';
import Footer from '../components/Footer';

const HomePage = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const userProfile = {
    name: 'John Doe',
    portfolioWorth: 10000,
  };

  const topCryptoData = [
    { id: 1, currency: 'Bitcoin', price: 50000 },
    { id: 2, currency: 'Ethereum', price: 3000 },
    // Add more crypto data
  ];

  const recentTransactions = [
    { id: 1, date: '2023-06-15', type: 'Buy', amount: 0.5 },
    { id: 2, date: '2023-06-14', type: 'Sell', amount: 1.2 },
    // Add more transactions
  ];

  const handleToggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="flex">
      {isSidebarOpen && (
        <aside className="bg-gray-200 h-screen w-1/5">
          {/* Sidebar content */}
          <nav className="py-4">
            <ul className="space-y-2">
              <li>
                <button
                  className="block px-4 py-2"
                  onClick={handleToggleSidebar}
                >
                  Close Sidebar
                </button>
              </li>
              {/* Add more sidebar items */}
            </ul>
          </nav>
        </aside>
      )}

      <div className="flex flex-col flex-grow">
        <Header />
        
        <div className="p-4">
          <h1 className="text-2xl font-bold mb-4">Home Page</h1>

          <Profile
            name={userProfile.name}
            portfolioWorth={userProfile.portfolioWorth}
          />

          <div className="mt-4">
            <h2 className="text-xl font-bold mb-2">Top 10 Cryptocurrencies</h2>
            <TopCryptoTable cryptoData={topCryptoData} />
          </div>

          <div className="mt-4">
            <h2 className="text-xl font-bold mb-2">Recent Transactions</h2>
            <TransactionTable transactions={recentTransactions} />
          </div>
        </div>

        <Footer />
      </div>
    </div>
  );
};

export default HomePage;
