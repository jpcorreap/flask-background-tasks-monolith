import { AppBar, Button, Link, Toolbar, Typography } from "@mui/material";

const NavBar = () => {
  return (
    <AppBar
      position="static"
      color="default"
      elevation={0}
      sx={{ borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}
    >
      <Toolbar sx={{ flexWrap: "wrap" }}>
        <Typography
          variant="h6"
          color="inherit"
          noWrap
          sx={{ flexGrow: 1, fontWeight: "bolder" }}
        >
          SuperVoices
        </Typography>
        <nav>
          <Link
            variant="button"
            color="text.primary"
            href="/signup"
            sx={{ my: 1, mx: 1.5 }}
          >
            Sign up
          </Link>
        </nav>
        <Button href="/login" variant="outlined" sx={{ my: 1, mx: 1.5 }}>
          Login
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
