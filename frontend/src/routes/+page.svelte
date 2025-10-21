<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, slide } from 'svelte/transition';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Alert from '$lib/components/ui/alert';
	import { Badge } from '$lib/components/ui/badge';

	const API_URL = 'http://localhost:8000';

	let message = '';
	let loading = false;
	let apiHealth = false;
	let modelInfo: any = null;
	let result: any = null;
	let errorMessage = '';
	let showResult = false;

	// Sample emails for quick testing
	const examples = [
		{
			label: 'Spam Example',
			text: 'WINNER! You have been selected to receive a $1000 Walmart gift card. Click here now to claim your prize before it expires!'
		},
		{
			label: 'Ham Example',
			text: 'hello, can we meet at the university at 2.00PM'
		}
	];

	onMount(async () => {
		await checkAPIHealth();
		await fetchModelInfo();
	});

	async function checkAPIHealth() {
		try {
			const response = await fetch(`${API_URL}/health`);
			const data = await response.json();
			apiHealth = data.model_loaded;
			errorMessage = '';
		} catch (error) {
			apiHealth = false;
			errorMessage =
				'Unable to connect to the API server. Please ensure it is running on port 8000.';
		}
	}

	async function fetchModelInfo() {
		try {
			const response = await fetch(`${API_URL}/model-info`);
			if (response.ok) {
				modelInfo = await response.json();
			}
		} catch (error) {
			console.error('Failed to fetch model info:', error);
		}
	}

	async function predict() {
		if (!message.trim()) {
			errorMessage = 'Please enter an email message to analyze';
			return;
		}

		loading = true;
		errorMessage = '';
		showResult = false;

		try {
			const response = await fetch(`${API_URL}/predict`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: message })
			});

			if (!response.ok) {
				throw new Error(`API error: ${response.statusText}`);
			}

			result = await response.json();
			showResult = true;
		} catch (error) {
			errorMessage = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
			result = null;
		} finally {
			loading = false;
		}
	}

	function clear() {
		message = '';
		result = null;
		errorMessage = '';
		showResult = false;
	}

	function loadExample(example: string) {
		message = example;
		result = null;
		showResult = false;
		errorMessage = '';
	}

	function handleKeydown(event: KeyboardEvent) {
		if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
			event.preventDefault();
			predict();
		}
	}
</script>

<svelte:head>
	<title>Email Spam Detector | ML-Powered Classification</title>
	<meta
		name="description"
		content="Classify emails as spam or legitimate using our Naive Bayes machine learning model"
	/>
</svelte:head>

<div class="bg-background min-h-screen">
	<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
		<!-- Header -->
		<header class="mb-12 text-center">
			<h1 class="tinos mb-3 mt-6 text-5xl font-bold tracking-tight">Email Spam Detector</h1>
			<p class="text-muted-foreground mx-auto max-w-2xl text-lg">
				Analyze email content in real-time using our Naive Bayes classifier trained on thousands of
				messages
			</p>
		</header>

		<!-- Status and Model Info -->
		<div class="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
			<!-- API Status Card -->
			<Card.Root class="border-l-4 {apiHealth ? 'border-l-primary' : 'border-l-destructive'}">
				<Card.Content class="pt-6">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<div class="bg-accent flex h-10 w-10 items-center justify-center rounded-full">
								{#if apiHealth}
									<svg
										class="text-primary h-5 w-5"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M5 13l4 4L19 7"
										/>
									</svg>
								{:else}
									<svg
										class="text-destructive h-5 w-5"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M6 18L18 6M6 6l12 12"
										/>
									</svg>
								{/if}
							</div>
							<div>
								<p class="text-muted-foreground text-sm font-medium">API Status</p>
								<p
									class="text-lg font-semibold"
									class:text-primary={apiHealth}
									class:text-destructive={!apiHealth}
								>
									{apiHealth ? 'Online' : 'Offline'}
								</p>
							</div>
						</div>
					</div>
				</Card.Content>
			</Card.Root>

			<!-- Model Stats -->
			{#if modelInfo}
				<Card.Root class="border-l-primary border-l-4">
					<Card.Content class="pt-6">
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<div class="bg-primary/10 flex h-10 w-10 items-center justify-center rounded-full">
									<svg
										class="text-primary h-5 w-5"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
										/>
									</svg>
								</div>
								<div>
									<p class="text-muted-foreground text-sm font-medium">Vocabulary</p>
									<p class="text-lg font-semibold">{modelInfo.vocabulary_size.toLocaleString()}</p>
								</div>
							</div>
						</div>
					</Card.Content>
				</Card.Root>

				<Card.Root class="border-l-accent border-l-4">
					<Card.Content class="pt-6">
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<div class="bg-accent flex h-10 w-10 items-center justify-center rounded-full">
									<svg
										class="text-accent-foreground h-5 w-5"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M13 10V3L4 14h7v7l9-11h-7z"
										/>
									</svg>
								</div>
								<div>
									<p class="text-muted-foreground text-sm font-medium">Spam Rate</p>
									<p class="text-lg font-semibold">
										{(modelInfo.prior_spam_probability * 100).toFixed(1)}%
									</p>
								</div>
							</div>
						</div>
					</Card.Content>
				</Card.Root>
			{/if}
		</div>

		<!-- Error Alert -->
		{#if errorMessage}
			<div transition:slide={{ duration: 300 }}>
				<Alert.Root class="mb-6" variant="destructive">
					<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<Alert.Title>Error</Alert.Title>
					<Alert.Description>{errorMessage}</Alert.Description>
				</Alert.Root>
			</div>
		{/if}

		<!-- Main Content Area -->
		<div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
			<!-- Input Section -->
			<div class="lg:col-span-2">
				<Card.Root class="shadow-lg">
					<Card.Header>
						<div class="flex items-center justify-between">
							<div>
								<Card.Title class="tinos text-xl">Analyze Email</Card.Title>
								<Card.Description class="mt-1">
									Paste or type an email message to check if it's spam
								</Card.Description>
							</div>
							{#if message.length > 0}
								<Badge variant="secondary" class="text-xs">
									{message.length} characters
								</Badge>
							{/if}
						</div>
					</Card.Header>
					<Card.Content class="space-y-4">
						<div class="relative">
							<Textarea
								id="message"
								placeholder="Paste your email content here...&#10;&#10;Try pasting a suspicious message or use one of the examples on the right →"
								bind:value={message}
								disabled={loading || !apiHealth}
								onkeydown={handleKeydown}
								class="min-h-[320px] resize-none transition-all focus:ring-2"
								rows={12}
							/>
							{#if !apiHealth}
								<div
									class="bg-background/80 absolute inset-0 flex items-center justify-center rounded-md backdrop-blur-sm"
								>
									<div class="text-center">
										<svg
											class="text-muted-foreground mx-auto h-12 w-12"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-2.83m-1.414 5.658a9 9 0 01-2.167-9.238m7.824 2.167a1 1 0 111.414 1.414m-1.414-1.414L3 3m8.293 8.293l1.414 1.414"
											/>
										</svg>
										<p class="text-muted-foreground mt-3 text-sm font-medium">API Offline</p>
										<p class="text-muted-foreground mt-1 text-xs">
											Start the server to enable classification
										</p>
									</div>
								</div>
							{/if}
						</div>

						<div class="flex flex-col gap-3 sm:flex-row">
							<Button
								onclick={predict}
								disabled={loading || !apiHealth || !message.trim()}
								class="flex-1 gap-2"
								size="lg"
							>
								{#if loading}
									<svg class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
										<circle
											class="opacity-25"
											cx="12"
											cy="12"
											r="10"
											stroke="currentColor"
											stroke-width="4"
										></circle>
										<path
											class="opacity-75"
											fill="currentColor"
											d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
										></path>
									</svg>
									Analyzing...
								{:else}
									<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
										/>
									</svg>
									Analyze Email
								{/if}
							</Button>
							<Button variant="outline" onclick={clear} disabled={loading} size="lg" class="gap-2">
								<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M6 18L18 6M6 6l12 12"
									/>
								</svg>
								Clear
							</Button>
						</div>

						<p class="text-muted-foreground text-xs">
							<kbd class="bg-muted rounded border px-1.5 py-0.5 text-xs">Cmd</kbd> +
							<kbd class="bg-muted rounded border px-1.5 py-0.5 text-xs">Enter</kbd> to analyze
						</p>
					</Card.Content>
				</Card.Root>
			</div>

			<!-- Examples Sidebar -->
			<div class="lg:col-span-1">
				<Card.Root>
					<Card.Header>
						<Card.Title class="tinos text-lg">Quick Examples</Card.Title>
						<Card.Description>Click to load sample emails</Card.Description>
					</Card.Header>
					<Card.Content class="space-y-3">
						{#each examples as example}
							<button
								onclick={() => loadExample(example.text)}
								disabled={loading}
								class="bg-card hover:border-primary hover:bg-accent w-full rounded-lg border p-4 text-left transition-all disabled:opacity-50"
							>
								<div class="mb-2 flex items-center gap-2">
									<Badge
										variant={example.label.includes('Spam') ? 'destructive' : 'default'}
										class="text-xs"
									>
										{example.label}
									</Badge>
								</div>
								<p class="text-muted-foreground line-clamp-3 text-sm">
									{example.text}
								</p>
							</button>
						{/each}

						<div class="bg-muted/50 mt-6 rounded-lg border p-4">
							<h4 class="mb-2 text-sm font-semibold">How it works</h4>
							<ul class="text-muted-foreground space-y-2 text-xs">
								<li class="flex gap-2">
									<span class="text-primary">•</span>
									<span>Naive Bayes algorithm analyzes word patterns</span>
								</li>
								<li class="flex gap-2">
									<span class="text-primary">•</span>
									<span>Trained on thousands of real emails</span>
								</li>
								<li class="flex gap-2">
									<span class="text-primary">•</span>
									<span>Returns confidence score with prediction</span>
								</li>
							</ul>
						</div>
					</Card.Content>
				</Card.Root>
			</div>
		</div>

		<!-- Results Section -->
		{#if showResult && result}
			<div transition:slide={{ duration: 400 }} class="mt-8 lg:col-span-3">
				<Card.Root
					class="overflow-hidden border-2 shadow-lg {result.is_spam
						? 'border-destructive'
						: 'border-primary'}"
				>
					<div class="bg-muted/50 px-6 py-4">
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<div
									class="flex h-14 w-14 items-center justify-center rounded-full shadow-lg"
									class:bg-destructive={result.is_spam}
									class:text-destructive-foreground={result.is_spam}
									class:bg-primary={!result.is_spam}
									class:text-primary-foreground={!result.is_spam}
								>
									{#if result.is_spam}
										<svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
											/>
										</svg>
									{:else}
										<svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
											/>
										</svg>
									{/if}
								</div>
								<div>
									<h3
										class="text-2xl font-bold"
										class:text-destructive={result.is_spam}
										class:text-primary={!result.is_spam}
									>
										{result.is_spam ? 'Spam Detected' : 'Legitimate Email'}
									</h3>
									<p class="text-muted-foreground text-sm">
										{result.is_spam ? 'This message appears to be spam' : 'This message looks safe'}
									</p>
								</div>
							</div>
							<div class="text-right">
								<div
									class="text-3xl font-bold"
									class:text-destructive={result.is_spam}
									class:text-primary={!result.is_spam}
								>
									{(result.confidence * 100).toFixed(1)}%
								</div>
								<p class="text-muted-foreground text-xs">Confidence</p>
							</div>
						</div>
					</div>

					<Card.Content class="pt-6">
						<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
							<!-- Word Count -->
							<div class="bg-card rounded-lg border p-4">
								<div class="flex items-center gap-3">
									<div class="bg-accent flex h-10 w-10 items-center justify-center rounded-full">
										<svg
											class="text-accent-foreground h-5 w-5"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
											/>
										</svg>
									</div>
									<div>
										<p class="text-2xl font-bold">{result.word_count}</p>
										<p class="text-muted-foreground text-xs">Words Analyzed</p>
									</div>
								</div>
							</div>

							<!-- Classification -->
							<div class="bg-card rounded-lg border p-4">
								<div class="flex items-center gap-3">
									<div
										class="bg-primary/10 flex h-10 w-10 items-center justify-center rounded-full"
									>
										<svg
											class="text-primary h-5 w-5"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
											/>
										</svg>
									</div>
									<div>
										<p class="text-2xl font-bold">{result.prediction}</p>
										<p class="text-muted-foreground text-xs">Classification</p>
									</div>
								</div>
							</div>

							<!-- Confidence Score -->
							<div class="bg-card rounded-lg border p-4">
								<div class="flex items-center gap-3">
									<div class="bg-muted flex h-10 w-10 items-center justify-center rounded-full">
										<svg
											class="text-muted-foreground h-5 w-5"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
											/>
										</svg>
									</div>
									<div>
										<p class="text-2xl font-bold">{result.confidence.toFixed(4)}</p>
										<p class="text-muted-foreground text-xs">Raw Score</p>
									</div>
								</div>
							</div>

							<!-- Keywords -->
							<div class="bg-card rounded-lg border p-4">
								<div class="flex items-center gap-3">
									<div class="bg-secondary flex h-10 w-10 items-center justify-center rounded-full">
										<svg
											class="text-secondary-foreground h-5 w-5"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"
											/>
										</svg>
									</div>
									<div>
										<p class="text-2xl font-bold">{result.cleaned_words.length}</p>
										<p class="text-muted-foreground text-xs">Keywords Found</p>
									</div>
								</div>
							</div>
						</div>

						<!-- Keywords Display -->
						<div class="bg-muted/30 mt-6 rounded-lg border p-4">
							<h4 class="mb-3 flex items-center gap-2 text-sm font-semibold">
								<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"
									/>
								</svg>
								Processed Keywords
							</h4>
							<div class="flex flex-wrap gap-2">
								{#each result.cleaned_words.slice(0, 15) as word, i}
									<Badge
										variant="secondary"
										class="animate-in fade-in"
										style="animation-delay: {i * 30}ms"
									>
										{word}
									</Badge>
								{/each}
								{#if result.cleaned_words.length > 15}
									<Badge variant="outline" class="font-normal">
										+{result.cleaned_words.length - 15} more keywords
									</Badge>
								{/if}
							</div>
						</div>
					</Card.Content>
				</Card.Root>
			</div>
		{/if}

		<!-- Footer / API Info -->
	</div>
	<footer class="mt-16 border-t px-[10%] py-10 pt-8">
		<div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
			<div>
				<h3 class="mb-3 text-sm font-semibold">Model Details</h3>
				<ul class="text-muted-foreground space-y-2 text-sm">
					<li class="flex items-center gap-2">
						<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
							/>
						</svg>
						Naive Bayes Classifier
					</li>
					<li class="flex items-center gap-2">
						<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
							/>
						</svg>
						{#if modelInfo}
							{modelInfo.vocabulary_size.toLocaleString()} vocabulary
						{:else}
							Loading model info...
						{/if}
					</li>
				</ul>
			</div>

			<div>
				<h3 class="mb-3 text-sm font-semibold">API Endpoint</h3>
				<div class="space-y-2">
					<div class="flex items-center gap-2">
						<div
							class="h-2 w-2 rounded-full"
							class:bg-primary={apiHealth}
							class:bg-destructive={!apiHealth}
							class:animate-pulse={apiHealth}
						></div>
						<span class="text-muted-foreground text-sm">
							{apiHealth ? 'Connected' : 'Disconnected'}
						</span>
					</div>
					<code class="bg-muted block rounded px-2 py-1 text-xs">{API_URL}</code>
				</div>
			</div>

			<div>
				<h3 class="mb-3 text-sm font-semibold">Resources</h3>
				<ul class="space-y-2 text-sm">
					<li>
						<a
							href="{API_URL}/docs"
							target="_blank"
							class="text-muted-foreground hover:text-primary flex items-center gap-2 transition-colors"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
								/>
							</svg>
							API Documentation
							<svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
								/>
							</svg>
						</a>
					</li>
					<li>
						<a
							href="{API_URL}/health"
							target="_blank"
							class="text-muted-foreground hover:text-primary flex items-center gap-2 transition-colors"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
								/>
							</svg>
							Health Check
						</a>
					</li>
				</ul>
			</div>

			<div>
				<h3 class="mb-3 text-sm font-semibold">About</h3>
				<p class="text-muted-foreground text-sm">
					ML-powered spam detection using natural language processing and statistical analysis to
					protect your inbox.
				</p>
			</div>
		</div>

		<div class="text-muted-foreground mt-8 border-t pt-6 text-center text-sm">
			<p>Built with Svelte 5 • FastAPI • scikit-learn</p>
		</div>
	</footer>
</div>
