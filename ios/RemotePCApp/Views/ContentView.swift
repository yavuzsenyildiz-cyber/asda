import SwiftUI

struct ContentView: View {
  @StateObject var viewModel = PCViewModel()
  @State private var isLoggedIn = false

  var body: some View {
    if isLoggedIn {
      TabView {
        ControlView()
          .tabItem {
            Label("Kontrol", systemImage: "power")
          }

        SettingsView()
          .tabItem {
            Label("Ayarlar", systemImage: "gear")
          }
      }
      .environmentObject(viewModel)
    } else {
      LoginView(isLoggedIn: $isLoggedIn)
        .environmentObject(viewModel)
    }
  }
}

#Preview {
  ContentView()
}
