/**
 * This represents some generic auth provider API, like Firebase.
 */
const authProvider = {
  isAuthenticated: false,
  signin(callback) {
    authProvider.isAuthenticated = true;
    setTimeout(callback, 100); // fake async
  },
  signout(callback) {
    authProvider.isAuthenticated = false;
    setTimeout(callback, 100); // fake async
  },
};

export { authProvider };
