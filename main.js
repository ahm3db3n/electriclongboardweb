import React, { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 w-full bg-white shadow-md flex justify-between items-center px-6 py-3">
      <div>
        <Button onClick={() => setIsMenuOpen(!isMenuOpen)}>Menu</Button>
        {isMenuOpen && (
          <div className="absolute top-12 left-0 bg-gray-100 shadow-md p-4 rounded-md">
            <Link href="/featured">Featured</Link>
            <Link href="/most-bought" className="block mt-2">Most Bought</Link>
            {/* Show Admin Dashboard for Admins */}
            <Link href="/admin" className="block mt-2 text-red-500">Admin Dashboard</Link>
          </div>
        )}
      </div>
      <h1 className="text-lg font-bold">Elecboardz</h1>
      <div>
        <Button onClick={() => setCartOpen(!cartOpen)}>Cart</Button>
        {cartOpen && (
          <Popover>
            <PopoverTrigger>Cart</PopoverTrigger>
            <PopoverContent>
              <p>Your cart is empty</p>
            </PopoverContent>
          </Popover>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
