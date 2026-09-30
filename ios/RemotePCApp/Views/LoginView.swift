import SwiftUI

struct LoginView: View {
  @EnvironmentObject var viewModel: PCViewModel
  @Binding var isLoggedIn: Bool

  @State private var deviceId = ""
  @State private var isLoading = false
  @State private var errorMessage = ""

  var body: some View {
    NavigationStack {
      VStack(spacing: 20) {
        Spacer()

        VStack(spacing: 10) {
          Image(systemName: "power.circle.fill")
            .font(.system(size: 60))
            .foregroundColor(.blue)

          Text("Bilgisayarı Aç")
            .font(.title)
            .fontWeight(.bold)
        }

        Spacer()

        VStack(spacing: 16) {
          TextField("Device ID", text: $deviceId)
            .textFieldStyle(.roundedBorder)
            .padding(.horizontal)
            .autocapitalization(.none)

          if !errorMessage.isEmpty {
            Text(errorMessage)
              .foregroundColor(.red)
              .font(.caption)
              .padding(.horizontal)
          }

          Button(action: login) {
            if isLoading {
              ProgressView()
                .tint(.white)
            } else {
              Text("Giriş Yap")
            }
          }
          .frame(maxWidth: .infinity)
          .padding()
          .background(Color.blue)
          .foregroundColor(.white)
          .cornerRadius(8)
          .padding(.horizontal)
          .disabled(deviceId.isEmpty || isLoading)
        }

        Spacer()
      }
      .navigationTitle("Giriş")
    }
  }

  private func login() {
    isLoading = true
    errorMessage = ""

    viewModel.login(deviceId: deviceId) { success, error in
      isLoading = false
      if success {
        isLoggedIn = true
      } else {
        errorMessage = error ?? "Giriş başarısız"
      }
    }
  }
}

#Preview {
  LoginView(isLoggedIn: .constant(false))
    .environmentObject(PCViewModel())
}
