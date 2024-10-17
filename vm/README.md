# Tutorial #0: Virtual Machine Setup
 
# Step 1: Establish connection using CS VPN
- Visit the website to establish connection to the cs VPN:
[Link to VPN Documentation](https://systems.cs.odu.edu/network/vpn/)

# Step 2: Login to VM
- The VM is hosted on the CS department
- Login using your CS username and password

 
## Step 3: 
- Once logged in, we are in an Ubuntu you should see the following screen.

Note that you do not have sudo privileges in this server, so we have to install everything manually

## Step 4: Install a GCC locally
- Download and install gcc from the source:
```bash
# Create directory for local installation
mkdir -p $HOME/local/bin $HOME/local/lib $HOME/local/include

# Download and extract `gcc` source code
wget http://ftp.gnu.org/gnu/gcc/gcc-9.3.0/gcc-9.3.0.tar.gz
tar -xf gcc-9.3.0.tar.gz
cd gcc-9.3.0

# Install dependencies required for GCC build
./contrib/download_prerequisites

# Create a build directory
mkdir build && cd build

# Configure and install GCC locally
../configure --prefix=$HOME/local --disable-multilib
make -j4
make install
```

- Add the installed gcc to your path:
```bash
export PATH="$HOME/local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"
```
- Verify gcc installation:
```bash
gcc --version
```
## Step 5: Reinstall Python with pyenv
- Now that gcc is available, go back to pyenv and re-run the installation:
```bash
pyenv install 3.9.7
```

Once we have that we can install packages required by the rest of the tutorials. 


