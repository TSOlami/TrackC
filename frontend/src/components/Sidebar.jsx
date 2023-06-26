import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <aside className="bg-gray-200 h-screen w-1/5">
      <nav className="py-4">
        <ul className="space-y-2">
          <li>
            <Link to="/home" className="block px-4 py-2">Home/Dashboard</Link>
          </li>
          <li>
            <Link to="/profile" className="block px-4 py-2">Profile</Link>
          </li>
          <li>
            <Link to="/about" className="block px-4 py-2">About Us</Link>
          </li>
          <li>
            <Link to="/support" className="block px-4 py-2">Support/Feedback</Link>
          </li>
          <li>
            <Link to="/logout" className="block px-4 py-2">Logout</Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
