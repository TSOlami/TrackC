import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = () => {
  const navigate = useNavigate();
  const [logoutError, setLogoutError] = useState(null);

  const handleLogout = async () => {
    try {
      const response = await fetch('/api/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Logout successful
        navigate('/');
      } else {
        // Handle logout error
        const data = await response.json();
        const { message } = data;
        setLogoutError(message);
      }
    } catch (error) {
      console.error('Error:', error);
      setLogoutError('An error occurred. Please try again later.');
    }
  };

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
      {logoutError && <p>{logoutError}</p>}
    </div>
  );
};

export default LogoutButton;
