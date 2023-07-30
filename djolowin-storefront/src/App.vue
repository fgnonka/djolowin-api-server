<template>
	<div id="wrapper">
		<nav class="navbar navbar-expand-lg navbar-dark bg-dark rounded" aria-label="Eleventh navbar example">
			<div class="container-fluid">
				<a class="navbar-brand" href="/">
					<img class="d-inline-block align-text-center" src="#" alt="Elephant Logo" width="40" height="40" />
					Djolo Win
				</a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse"
					data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
					aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="navbarSupportedContent">
					<ul class="navbar-nav me-auto mb-2 mb-lg-0">
						<li class="nav-item">
							<a class="nav-link m-0" href="#" type="button" data-bs-toggle="dropdown" aria-expanded="false">
								<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="gray"
									class="bi bi-bell-fill bell-icon" viewBox="0 0 16 16">
									<path
										d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z" />
								</svg>
							</a>
							<div class="dropdown-menu " aria-labelledby="navbarDropdown">
								<div class="dropdown-item">
								</div>
							</div>
						</li>
						<li class="nav-item dropdown">
							<a class="nav-link dropdown-toggle" href="#" id="dropdownMenuLink" role="button"
								data-bs-toggle="dropdown" aria-expanded="false">
								<i class="fa fa-user"></i>User</a>
							<div class="dropdown-menu" aria-labelledby="navbarDropdown">
								<a class="dropdown-item" href="{% url 'djolowin_profile:profile' %}">My DjoloWin</a>
								<div class="dropdown-divider"></div>
								<a class="dropdown-item" href="{% url 'account:user-detail' uuid=request.user.uuid %}">My
									Profile Information</a>
								<div class="dropdown-divider"></div>
								<a class="dropdown-item" href="{% url 'playercard:owned-playercard' %}">My Cards</a>
								<a class="dropdown-item" href="{% url 'collection:collection_list' %}">My Collections</a>
								<a class="dropdown-item" href="{% url 'auction:owned_auctions' %}">My Auctions</a>
								<a class="dropdown-item" href="{% url 'wallet:wallet-dashboard' %}">My Wallet</a>
							</div>
						</li>
						<li class="nav-item dropdown">
							<a class="nav-link dropdown-toggle text-wrap" href="#" role="button" data-bs-toggle="dropdown"
								aria-expanded="false">
								Cards Market
							</a>
							<div class="dropdown-menu" aria-labelledby="navbarDropdown">
								<a class="dropdown-item" href="#">Auctions</a>
								<a class="dropdown-item" href="/allplayercards">Cards on Sale</a>
								<a class="dropdown-item" href="#">Bundles</a>
								<a class="dropdown-item" href="#">Special Offers</a>
							</div>
						</li>
						<li>
							<a class="nav-link disabled" href="#" role="button" data-bs-toggle="dropdown"
								aria-expanded="false">
								DjoloWin Shop
							</a>
						</li>
						<li class="nav-item dropdown">
							<a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
								aria-expanded="false">
								Settings
							</a>
							<div class="dropdown-menu" aria-labelledby="navbarDropdown">
								<a class="dropdown-item" href="#">Privacy Settings</a>
								<a class="dropdown-item" href='#'>Notifications Settings</a>
								<a class="dropdown-item" href="#">Security</a>
								<a class="dropdown-item" href="#">Payment Methods</a>
								<a class="dropdown-item" href="#">Language and Location</a>
							</div>
						</li>
						<li class="nav-item">
							<a href="#" class="nav-link"><i class="fa fa-fw fa-power-off"></i>Log Out</a>
						</li>
					</ul>
					<form class="d-flex" role="search">
						<input class="form-control" type="search" placeholder="Search" aria-label="Search" />
					</form>
				</div>
			</div>
		</nav>
		
	</div>
	<router-view/>
</template>

<style>
.loading-spinner {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 100vh;
}

.spinner {
	color: aliceblue;
}
</style>




