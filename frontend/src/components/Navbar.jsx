import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 py-4 px-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to="/" className="text-white text-lg font-semibold">My App</Link>
        </div>
        <div className="space-x-4">
          <Link to="/login" className="text-white">Login</Link>
          <Link to="/signup" className="text-white">Sign Up</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;