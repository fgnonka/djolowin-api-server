<template>
	<div id="document">
		<div id="wrapper" class="wrapping">
			<NavBar class="mb-4" />
			<div class="container-lg">
				<router-view></router-view>
			</div>
		</div>
		<Footer />
	</div>
</template>

<script setup>
import Footer from './components/Footer.vue';
import NavBar from './components/NavBar.vue';
</script>


<style>
@import './assets/css/main.css';

</style>

<script>

</script>



