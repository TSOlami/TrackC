import { useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import Profile from '../components/Profile';
import TopCryptoTable from '../components/TopCryptoTable';
import TransactionTable from '../components/TransactionTable';
import Footer from '../components/Footer';
import LogoutButton from '../components/LogoutButton';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Transaction from "../components/Transaction";


const HomePage = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [userData, setUserData] = useState(null);
  const [transactionData, setTransactionData] = useState(null);
  const [cryptoData, setCryptoData] = useState([]);
  const { user_id } = useParams();

  const userProfile = {
    name: 'John Doe',
    portfolioWorth: 10000,
  };

  // Fetch transaction data from the '/<user_id>/transactions' endpoint
  const fetchTransactionData = async () => {
    try {
      const response = await fetch(`http://localhost:5000/${user_id}/transactions`);
      const data = await response.json();
      setTransactionData(data);
      console.log(data)
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleToggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  useEffect(() => {
    // Fetch user data using the userId from the backend
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/home/${user_id}`);
        const data = await response.json();
        setUserData(data);
        setCryptoData(data.results);
        console.log(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    

    fetchUserData();
    fetchTransactionData();
  }, [user_id]);

  return (
    <>
      <Header />
      <div>
        <div className="grid grid-cols-1 sm:grid-cols-2 h-screen">
          {isSidebarOpen && <Sidebar />}

          <div className="flex flex-col justify-center items-center p-4">
            <h1 className="text-2xl font-bold mb-4">Home Page</h1>

            <button
              className="block px-4 py-2 mb-4"
              onClick={handleToggleSidebar}
            >
              {isSidebarOpen ? 'Close Sidebar' : 'Open Sidebar'}
            </button>

            {userData && (
              <Profile
                username={userData.name}
                portfolioWorth={userData.portfolioWorth}
            />
            )}
            
            <div className="mt-4">
              <h2 className="text-xl font-bold mb-2">Recent Transactions</h2>
              {transactionData && transactionData.length > 0 ? (
                <TransactionTable transactions={recentTransactions} />
              ) : (
                <p>No recent transactions</p>
              )}
            </div>

            <div className="mt-4">
              <h2 className="text-xl font-bold mb-2">Top 10 Cryptocurrencies</h2>
              <TopCryptoTable cryptoData={cryptoData} />
            </div>
      
            <div className="mt-4">
              <h2 className="text-xl font-bold mb-2">Enter Transaction Details</h2>
              <Transaction user_id={user_id} />
            </div>
            
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default HomePage;