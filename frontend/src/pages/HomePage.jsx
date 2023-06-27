import { useState } from 'react';
import { Link } from 'react-router-dom';
import Profile from '../components/Profile';
import TopCryptoTable from '../components/TopCryptoTable';
import TransactionTable from '../components/TransactionTable';
import Footer from '../components/Footer';
import LogoutButton from '../components/LogoutButton';

const HomePage = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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
    <div className="grid grid-cols-1 sm:grid-cols-2 h-screen">
      {isSidebarOpen && (
        <aside className="bg-gray-200">
          {/* Sidebar content */}
          <nav className="py-4">
            <ul className="space-y-2">
              <li>
                <Link to="/home" className="block px-4 py-2">
                  Home/Dashboard
                </Link>
              </li>
              <li>
                <Link to="/profile" className="block px-4 py-2">
                  Profile
                </Link>
              </li>
              <li>
                <Link to="/about" className="block px-4 py-2">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/support" className="block px-4 py-2">
                  Support/Feedback
                </Link>
              </li>
              <li>
                <LogoutButton /> {/* Render the LogoutButton component */}
              </li>
            </ul>
          </nav>
        </aside>
      )}

      <div className="flex flex-col justify-center items-center p-4">
        <h1 className="text-2xl font-bold mb-4">Home Page</h1>

        <button
          className="block px-4 py-2 mb-4"
          onClick={handleToggleSidebar}
        >
          {isSidebarOpen ? 'Close Sidebar' : 'Open Sidebar'}
        </button>

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
  );
};

export default HomePage;
