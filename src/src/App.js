import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';
import TextField from '@material-ui/core/TextField';
import IconButton from '@material-ui/core/IconButton';
import LinkedInIcon from '@material-ui/icons/LinkedIn';
import GitHubIcon from '@material-ui/icons/GitHub';
import EmailIcon from '@material-ui/icons/Email';

const useStyles = makeStyles((theme) => ({
  appBar: {
    marginBottom: theme.spacing(4),
  },
  avatarContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: theme.spacing(2),
  },
  avatar: {
    width: '15vw',
    height: '15vw',
  },
  intro: {
    textAlign: 'center',
    marginBottom: theme.spacing(4),
  },
  divider: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  projectCard: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    padding: '20px',
  },
  projectImage: {
    height: 150,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  },
  projectTitle: {
    fontWeight: 'bold',
    marginBottom: theme.spacing(1),
  },
  projectDescription: {
    flexGrow: 1,
    marginBottom: theme.spacing(1),
  },
  projectLinks: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  contactContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: theme.spacing(4),
  },
  form: {
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  formField: {
    margin: theme.spacing(1),
    width: '90%',
  },
  socialIcons: {
    display: 'flex',
    justifyContent: 'center',
  },
  footer: {
    display: 'flex',
    justifyContent: 'center',
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(2),
  },
}));

function App() {
  const classes = useStyles();

  return (
    <>
      <AppBar position="static" className={classes.appBar}>
        <Toolbar>
          <Typography variant="h6">Portfolio</Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md">
        <div className={classes.avatarContainer}>
          <Avatar alt="Profile Picture" src="/default_pp.jpg" className={classes.avatar} />
        </div>
        <div className={classes.intro}>
          <Typography variant="h5">John Doe</Typography>
          <Typography variant="subtitle1">Full Stack Web Developer</Typography>
          <Typography variant="body1">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam aliquet sagittis enim, sit amet dignissim nibh
            pharetra ut.
          </Typography>
        </div>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Paper>
              <Button component="a" href="/projects">
                Projects
              </Button>
            </Paper>
          </Grid>
        <Grid item xs={12}>
          <Grid container spacing={4}>
            <Grid item xs={12} sm={6} md={4}>
              <Paper className={classes.projectCard} >
                <div
                  className={classes.projectImage}
                  style={{ backgroundImage: "url('https://picsum.photos/250/150')" }}
                />
                <div className={classes.projectContent}>
                  <Typography variant="h6" className={classes.projectTitle}>
                    Project 1
                  </Typography>
                  <Typography variant="body1" className={classes.projectDescription}>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ut blandit leo.
                  </Typography>
                  <div className={classes.projectLinks}>
                    <Button component="a" href="/project1">
                      View Project
                    </Button>
                    <Button component="a" href="/project1/code">
                      View Code
                    </Button>
                  </div>
                </div>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper className={classes.projectCard}>
                <div
                  className={classes.projectImage}
                  style={{ backgroundImage: "url('https://picsum.photos/250/150?blur')" }}
                />
                <div className={classes.projectContent}>
                  <Typography variant="h6" className={classes.projectTitle}>
                    Project 2
                  </Typography>
                  <Typography variant="body1" className={classes.projectDescription}>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ut blandit leo.
                  </Typography>
                  <div className={classes.projectLinks}>
                    <Button component="a" href="/project2">
                      View Project
                    </Button>
                    <Button component="a" href="/project2/code">
                      View Code
                    </Button>
                  </div>
                </div>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper className={classes.projectCard}>
                <div
                  className={classes.projectImage}
                  style={{ backgroundImage: "url('https://picsum.photos/250/150?grayscale')" }}
                />
                <div className={classes.projectContent}>
                  <Typography variant="h6" className={classes.projectTitle}>
                    Project 3
                  </Typography>
                  <Typography variant="body1" className={classes.projectDescription}>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ut blandit leo.
                  </Typography>
                  <div className={classes.projectLinks}>
                    <Button component="a" href="/project3">
                      View Project
                    </Button>
                    <Button component="a" href="/project3/code">
                      View Code
                    </Button>
                  </div>
                </div>
              </Paper>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12}>
          <div className={classes.contactContainer}>
            <Typography variant="h5" gutterBottom>
              Contact Me
            </Typography>
            <form className={classes.form}>
              <TextField
                label="Name"
                variant="outlined"
                className={classes.formField}
              />
              <TextField
                label="Email"
                variant="outlined"
                className={classes.formField}
              />
              <TextField
                label="Message"
                variant="outlined"
                multiline
                rows={4}
                className={classes.formField}
              />
              <Button variant="contained" color="primary">
                Send Message
              </Button>
            </form>
            <div className={classes.socialIcons}>
              <IconButton href="https://www.linkedin.com/in/johndoe">
                <LinkedInIcon />
              </IconButton>
              <IconButton href="https://github.com/johndoe">
                <GitHubIcon />
              </IconButton>
              <IconButton href="mailto:johndoe@example.com">
                <EmailIcon />
              </IconButton>
            </div>
          </div>
        </Grid>
      </Grid>
  </Container>
  <footer className={classes.footer}>
    <Typography variant="body2">© 2023 John Doe</Typography>
  </footer>
  </>
);
  }

export default App;
